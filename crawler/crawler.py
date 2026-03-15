"""Simple site-restricted web crawler.

This crawler starts from a base URL, discovers links on each page,
and only crawls pages that stay on the same site (same scheme + host).
"""

# Enable modern type-hint syntax (e.g., str | None) on older Python 3 versions.
from __future__ import annotations

# Standard library modules for CLI parsing, queue/deque, and stderr exits.
import argparse
import collections
import concurrent.futures
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
# Built-in HTML parser we can subclass to collect links without extra dependencies.
from html.parser import HTMLParser
# Type hints used for readability and editor support.
from typing import Deque, Iterable, List, Set
# URL utilities for joining relative links and splitting/rebuilding URL parts.
from urllib.parse import urljoin, urlsplit, urlunsplit
# HTTP request helpers from standard library.
from urllib.request import Request, urlopen


class LinkExtractor(HTMLParser):
	"""Extracts href values from anchor tags."""

	def __init__(self) -> None:
		# Initialize HTMLParser internals.
		super().__init__()
		# Store every href encountered while parsing one HTML document.
		self.links: List[str] = []

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
		# We only care about <a ...> tags because those represent navigational links.
		if tag.lower() != "a":
			return

		# attrs is a list like [("href", "/about"), ("class", "btn")].
		for key, value in attrs:
			# Keep only href values that are non-empty.
			if key.lower() == "href" and value:
				self.links.append(value)


class PageTextExtractor(HTMLParser):
	"""Extracts visible text and title from an HTML page.

	Filtering is intentionally conservative to avoid dropping useful content.
	Only clearly non-content tags are skipped.
	"""

	# Tags that almost never contain useful natural-language page content for RAG.
	HARD_SKIP_TAGS = {
		"script",
		"style",
		"noscript",
		"svg",
		"canvas",
		"template",
	}

	def __init__(self) -> None:
		super().__init__()
		self.text_chunks: List[str] = []
		self.title_chunks: List[str] = []
		self.skip_depth = 0
		self.skip_stack: list[bool] = []
		self.in_title = False

	def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
		tag_name = tag.lower()

		if tag_name == "title":
			self.in_title = True

		should_skip = tag_name in self.HARD_SKIP_TAGS

		self.skip_stack.append(should_skip)
		if should_skip:
			self.skip_depth += 1

	def handle_endtag(self, tag: str) -> None:
		tag_name = tag.lower()

		if tag_name == "title":
			self.in_title = False

		if self.skip_stack:
			was_skipped = self.skip_stack.pop()
			if was_skipped and self.skip_depth > 0:
				self.skip_depth -= 1

	def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
		# Handle self-closing tags in a balanced way with skip stack tracking.
		self.handle_starttag(tag, attrs)
		self.handle_endtag(tag)

	def handle_data(self, data: str) -> None:
		# Keep title text regardless of skip rules so metadata remains available.
		if self.in_title:
			self.title_chunks.append(data)

		# Ignore all content under skipped regions.
		if self.skip_depth > 0:
			return

		clean = data.strip()
		if clean:
			self.text_chunks.append(clean)

	def get_title(self) -> str:
		raw = " ".join(self.title_chunks)
		return re.sub(r"\s+", " ", raw).strip()

	def get_text(self) -> str:
		raw = " ".join(self.text_chunks)
		return re.sub(r"\s+", " ", raw).strip()


@dataclass
class FetchResult:
	"""Represents the result of one URL fetch attempt."""

	url: str
	html: str | None
	status_code: int | None
	content_type: str | None
	content_length_bytes: int | None
	error: str | None


def normalize_url(raw_url: str) -> str:
	"""Normalize URLs to reduce duplicate crawling.

	- strips fragment
	- normalizes empty path to '/'
	- keeps query strings (they may point to different resources)
	"""
	# Break URL into parts: scheme, netloc, path, query, fragment.
	parts = urlsplit(raw_url)
	# Normalize empty path (e.g., https://example.com) to '/'.
	path = parts.path or "/"
	# Rebuild URL with normalized scheme/host and no fragment.
	# Lowercasing scheme/host avoids duplicates due to case variations.
	return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


def is_same_site(candidate: str, base: str) -> bool:
	"""Return True if candidate is on the same scheme+host as base."""
	# Parse both URLs so we can compare site identity safely.
	c = urlsplit(candidate)
	b = urlsplit(base)
	# Site boundary rule: exact same scheme and host.
	# Example: https://docs.example.com is NOT the same as https://example.com.
	return c.scheme.lower() == b.scheme.lower() and c.netloc.lower() == b.netloc.lower()


def host_is_allowed(host: str, allowed_domains: set[str]) -> bool:
	"""Return True when host is exactly in, or a subdomain of, an allowed domain."""
	host = host.lower()
	for domain in allowed_domains:
		domain = domain.lower()
		if host == domain or host.endswith(f".{domain}"):
			return True
	return False


def fetch_html(url: str, timeout: int = 10) -> FetchResult:
	"""Fetch URL and return payload + metadata for success/failure handling."""
	# Build an HTTP request with explicit headers for polite/content-focused crawling.
	request = Request(
		url,
		headers={
			# Identify the client. Some sites block requests without a User-Agent.
			"User-Agent": "SimpleSiteCrawler/1.0 (+https://example.local)",
			# Ask for HTML-type responses.
			"Accept": "text/html,application/xhtml+xml",
		},
	)

	try:
		# Open the URL; context manager ensures socket/response is closed.
		with urlopen(request, timeout=timeout) as response:
			status_code = getattr(response, "status", None)
			# Check response content type so we skip binary files (PDF/image/etc.).
			content_type = response.headers.get("Content-Type", "").lower()
			data = response.read()
			content_length_bytes = len(data)

			if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
				return FetchResult(
					url=url,
					html=None,
					status_code=status_code,
					content_type=content_type,
					content_length_bytes=content_length_bytes,
					error="non-html-content",
				)

			# Use declared charset when available; fallback to UTF-8.
			charset = response.headers.get_content_charset() or "utf-8"
			# Decode bytes to text; replace malformed bytes instead of crashing.
			decoded = data.decode(charset, errors="replace")
			return FetchResult(
				url=url,
				html=decoded,
				status_code=status_code,
				content_type=content_type,
				content_length_bytes=content_length_bytes,
				error=None,
			)
	except Exception:
		# Network errors, SSL errors, decode errors, etc. are treated as non-fatal.
		# Returning None lets crawler continue with other pages.
		return FetchResult(
			url=url,
			html=None,
			status_code=None,
			content_type=None,
			content_length_bytes=None,
			error="request-failed",
		)


def extract_links(page_url: str, html: str) -> Iterable[str]:
	"""Extract and absolutize links from HTML."""
	# Parse one page's HTML and collect raw href values.
	parser = LinkExtractor()
	parser.feed(html)
	# Close parser to flush any buffered parse state.
	parser.close()

	# Convert each raw href into a normalized absolute URL.
	for href in parser.links:
		# Resolve relative links against the current page URL.
		absolute = urljoin(page_url, href)
		# Split so we can inspect scheme before yielding.
		parts = urlsplit(absolute)

		# Only follow web links.
		if parts.scheme.lower() not in {"http", "https"}:
			continue

		# Yield normalized URL so queue/visited duplicate checks are reliable.
		yield normalize_url(absolute)


def extract_text_and_title(html: str) -> tuple[str, str]:
	"""Return (title, cleaned_text) extracted from an HTML document."""
	parser = PageTextExtractor()
	parser.feed(html)
	parser.close()
	return parser.get_title(), parser.get_text()


def now_utc_iso() -> str:
	"""Return an ISO-8601 UTC timestamp with trailing Z."""
	return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def crawl_site(
	base_url: str,
	max_pages: int = 200,
	workers: int = 8,
	allowed_domains: set[str] | None = None,
) -> dict:
	"""Crawl from base_url, extract text+metadata, and return JSON-ready payload."""
	# Normalize start URL once so later comparisons use consistent formatting.
	base_url = normalize_url(base_url)

	# Guardrail: this crawler only supports HTTP/S URLs.
	if urlsplit(base_url).scheme not in {"http", "https"}:
		raise ValueError("Base URL must start with http:// or https://")

	base_host = urlsplit(base_url).netloc.lower()

	# If whitelist not provided, default to base host only.
	if allowed_domains is None or len(allowed_domains) == 0:
		allowed_domains = {base_host}
	else:
		allowed_domains = {d.lower().strip() for d in allowed_domains if d.strip()}

	if not host_is_allowed(base_host, allowed_domains):
		raise ValueError("Base URL host is not in allowed domains")

	if workers <= 0:
		raise ValueError("workers must be a positive integer")

	# visited tracks pages we've already processed.
	visited: Set[str] = set()
	# queue stores pages waiting to be processed (BFS order).
	queue: Deque[str] = collections.deque([base_url])
	# Keep track of URLs already queued to reduce duplicates before processing.
	queued: Set[str] = {base_url}

	pages: list[dict] = []
	failed_pages: list[dict] = []
	in_flight: Set[str] = set()

	# A small thread pool improves crawl throughput because page fetches are I/O-bound.
	with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
		# Continue until no work remains or we hit max_pages safety limit.
		while queue and len(visited) < max_pages:
			batch: list[str] = []

			# Pull the next wave of URLs in BFS order, bounded by worker count.
			while queue and len(batch) < workers and (len(visited) + len(batch)) < max_pages:
				candidate = queue.popleft()
				if candidate in visited or candidate in in_flight:
					continue
				in_flight.add(candidate)
				batch.append(candidate)

			if not batch:
				continue

			future_to_url = {executor.submit(fetch_html, url): url for url in batch}

			for future in concurrent.futures.as_completed(future_to_url):
				current = future_to_url[future]
				in_flight.discard(current)

				try:
					fetch_result = future.result()
				except Exception:
					fetch_result = FetchResult(
						url=current,
						html=None,
						status_code=None,
						content_type=None,
						content_length_bytes=None,
						error="request-failed",
					)

				# Mark as visited regardless of fetch result to avoid infinite retries.
				visited.add(current)

				# Skip link extraction when fetch failed or content was non-HTML.
				if fetch_result.html is None:
					failed_pages.append(
						{
							"url": current,
							"error": fetch_result.error,
							"status_code": fetch_result.status_code,
							"content_type": fetch_result.content_type,
							"crawl_timestamp_utc": now_utc_iso(),
						}
					)
					continue

				title, text = extract_text_and_title(fetch_result.html)
				outbound_links = set(extract_links(current, fetch_result.html))

				pages.append(
					{
						"url": current,
						"title": title,
						"text": text,
						"crawl_timestamp_utc": now_utc_iso(),
						"status_code": fetch_result.status_code,
						"content_type": fetch_result.content_type,
						"word_count": len(text.split()),
						"outbound_link_count": len(outbound_links),
					}
				)

				# Discover links from the page and enqueue valid internal URLs.
				for link in outbound_links:
					# No need to enqueue links we've already crawled.
					if link in visited:
						continue

					link_host = urlsplit(link).netloc.lower()
					# Enforce whitelist boundary so crawler never leaves approved domains.
					if not host_is_allowed(link_host, allowed_domains):
						continue

					# Avoid queue duplicates.
					if link in queued:
						continue
					queued.add(link)
					# Add to queue for future crawling.
					queue.append(link)

	# Return JSON-ready crawl payload for persistence and downstream RAG loading.
	return {
		"crawl_started_from": base_url,
		"allowed_domains": sorted(allowed_domains),
		"max_pages": max_pages,
		"workers": workers,
		"pages": pages,
		"failed_pages": failed_pages,
		"summary": {
			"visited_url_count": len(visited),
			"success_count": len(pages),
			"failed_count": len(failed_pages),
		},
	}


def save_json(output_path: str, payload: dict) -> None:
	"""Write payload to disk as pretty JSON, creating folders if needed."""
	dirname = os.path.dirname(output_path)
	if dirname:
		os.makedirs(dirname, exist_ok=True)
	with open(output_path, "w", encoding="utf-8") as f:
		json.dump(payload, f, ensure_ascii=False, indent=2)


def parse_args() -> argparse.Namespace:
	# Configure command-line interface.
	parser = argparse.ArgumentParser(description="Simple same-site web crawler")
	# Required positional argument: where crawling begins.
	parser.add_argument("base_url", help="Starting URL, e.g. https://example.com")
	# Optional cap to prevent runaway crawls.
	parser.add_argument(
		"--max-pages",
		type=int,
		default=200,
		help="Maximum pages to crawl (default: 200)",
	)
	parser.add_argument(
		"--output",
		default="Crawler/data/site_pages.json",
		help="Output JSON path (default: Crawler/data/site_pages.json)",
	)
	parser.add_argument(
		"--workers",
		type=int,
		default=8,
		help="Number of concurrent fetch workers (default: 8)",
	)
	parser.add_argument(
		"--allowed-domain",
		action="append",
		default=[],
		help=(
			"Allowed domain whitelist entry; repeat flag to add multiple. "
			"Matches exact domain and subdomains. If omitted, base host is used."
		),
	)
	# Parse and return CLI args namespace.
	return parser.parse_args()


def main() -> int:
	# Start timer for overall crawl duration measurement.
	start_time = datetime.now()

	# Read arguments from command line.
	args = parse_args()

	# Validate max-pages early and provide meaningful exit code on bad input.
	if args.max_pages <= 0:
		print("--max-pages must be a positive integer", file=sys.stderr)
		return 2
	if args.workers <= 0:
		print("--workers must be a positive integer", file=sys.stderr)
		return 2

	try:
		# Execute crawl and collect structured page records.
		result = crawl_site(
			args.base_url,
			max_pages=args.max_pages,
			workers=args.workers,
			allowed_domains=set(args.allowed_domain),
		)
	except ValueError as exc:
		# Input validation errors are printed for the user and return non-zero.
		print(str(exc), file=sys.stderr)
		return 2

	save_json(args.output, result)

	# Print crawled URLs to stdout (useful for piping to files/tools).
	for page in result["pages"]:
		print(page["url"])

	# Print summary to stderr so stdout remains clean URL output.
	end_time = datetime.now()
	duration = end_time - start_time
	time_per_page = duration / max(result["summary"]["visited_url_count"], 1)
	print(
		(
			f"\nSaved crawl output to {args.output}. "
			f"Success: {result['summary']['success_count']}, "
			f"Failed: {result['summary']['failed_count']}, "
			f"Visited: {result['summary']['visited_url_count']}, "
			f"Duration: {duration}, "
			f"Time per page: {time_per_page}."
		),
		file=sys.stderr,
	)
	# Return success.
	return 0


if __name__ == "__main__":
	# Exit process with the status code returned by main().
	raise SystemExit(main())
