# Import Hugging Face inference client used to call hosted chat models.
from huggingface_hub import InferenceClient
# Import model configuration values and API token.
from config import BASE_MODEL, MY_MODEL, HF_TOKEN
# Import structured source data used for retrieval-augmented prompting.
from src.bps_data_v2 import DISTRICT_SOURCES, DISTRICT_FACTS, GRADE_RULES, PROGRAM_RULES, SCHOOL_RECORDS, SEI_LANGUAGE_SPECIFIC_EXAMPLES

# Load the summary data from scraping and cleaning the BPS sites in src/summary.json
with open("src/summary.json", "r", encoding="utf-8") as f:
    SUMMARY_DATA = f.read()


# Load in the bps_chatbot_conversation_example.txt file as a string to use as an example prompt in the UI.
with open("src/bps_chatbot_conversation_example.txt", "r", encoding="utf-8") as f:
    EXAMPLE_CONVERSATION = f.read()

# Load in the background information in the BPS_background.txt file as a string to use as an example prompt in the UI.
with open("src/BPS_background.txt", "r", encoding="utf-8") as f:
    BPS_BACKGROUND = f.read()

# improved system prompt, which directs to bps_data, rather than including data directly here
# High-level behavior instructions sent as the first system message.
SYSTEM_PROMPT = f"""
You are a Boston Public Schools enrollment helper.

Your job is to help families understand school options and enrollment steps using only the source information provided to you.

Rules:
- Only use facts contained in the provided source information.
- Do not invent school details, eligibility rules, contact information, tour schedules, transportation details, or program offerings.
- If the user has not provided enough information, ask a short follow-up question.
- If the source information does not support a confident answer, say so clearly.
- When relevant, separate:
  1. what is known from the source,
  2. what is still missing,
  3. what the family should verify with BPS.
  4. urls or contact info for next steps if available in the source information.
- Be warm, concise, and helpful.
- If the question is unrelated to Boston Public Schools, politely redirect.

Helpful guidance:
- Important details may include grade level, child age, home address or neighborhood, language preferences, and special program needs.
- Do not claim a school is definitely available unless the provided source information supports that.
- Remeber that enrollment rules can be complex and may have exceptions, so it's important to be clear about what is known vs unknown based on the source information.
- Remeber that not all families will speak English as a first language, so be prepared to ask clarifying questions about language preferences and provide information about language programs when relevant.
- If you are unsure about what the user is asking, ask a clarifying question to get more information before attempting to answer.

Below is an example conversation that demonstrates how to use the provided source information to answer user questions. Note how the assistant cites specific facts from the sources, identifies missing information, 
and provides clear next steps for the family to verify with BPS. In the example you are the "bot" and the user is the "user". The assistant always tries to use the provided source information to answer the user's question, 
if the source information does not contain the answer, use what you know from training. If you don't know the answer, say you don't know and suggest next steps for the user to find out.

{EXAMPLE_CONVERSATION}

Finally, here is some background information about Boston Public Schools that may be helpful for you to reference when answering questions:

{BPS_BACKGROUND}

"""

# Chatbot wrapper class that handles retrieval, prompt formatting, and response calls.
class Chatbot:
    """
    This class is extra scaffolding around a model. Modify this class to specify how the model recieves prompts and generates responses.

    Example usage:
        chatbot = Chatbot()
        response = chatbot.get_response("What options are available for me?")
    """

    def __init__(self):
        """
        Initialize the chatbot with a HF model ID
        """
        # Prefer fine-tuned/custom model if set, otherwise use base model.
        model_id = MY_MODEL if MY_MODEL else BASE_MODEL # define MY_MODEL in config.py if you create a new model in the HuggingFace Hub
        # Create API client bound to chosen model and auth token.
        self.client = InferenceClient(model=model_id, token=HF_TOKEN)

    # Normalize text consistently for simple keyword matching.
    def _normalize_text(self, text):
        # Lowercase and trim whitespace; return empty string for falsey input.
        return text.lower().strip() if text else ""

    # Build retrieval terms from current question plus limited recent history.
    def _extract_query_terms(self, user_input, history=None):
        """
        Build a small bag of query terms from the current user input and recent history.
        This is a lightweight retrieval helper, not full NLP.
        """
        # Start with the latest user message.
        combined = user_input or ""

        # Include up to the last 3 history turns to preserve short-term context.
        if history:
            for item in history[-3:]:
                # Handle tuple/list format like (user, assistant).
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    combined += " " + str(item[0]) + " " + str(item[1])
                # Handle message-dict format like {"role": ..., "content": ...}.
                elif isinstance(item, dict):
                    combined += " " + str(item.get("content", ""))
                # Fallback for any other history object shape.
                else:
                    combined += " " + str(item)

        # Canonicalize text before term extraction.
        text = self._normalize_text(combined)

        # basic synonym expansion
        # Add equivalent terms to improve recall for simple keyword retrieval.
        replacements = {
            "kindergarten": "k2 kindergarten",
            "prek": "pre-k pre k k0 k1",
            "pre-k": "pre-k pre k k0 k1",
            "spanish": "spanish dual language bilingual",
            "bilingual": "bilingual dual language",
            "special ed": "special education inclusion disabilities",
            "special education": "special education inclusion disabilities",
            "disability": "disabilities inclusion",
            "esl": "esl english learner sei",
            "english learner": "esl english learner sei",
        }

        # Begin with normalized text and append synonym expansions where matched.
        expanded = text
        for key, value in replacements.items():
            if key in text:
                expanded += " " + value

        # Return unique tokens as a set for fast membership tests.
        return set(expanded.split())

    # Convert a dict record into one searchable normalized text string.
    def _record_to_text(self, record):
        """
        Flatten a record into searchable text.
        """
        # Accumulate string versions of all record values.
        parts = []
        for value in record.values():
            # Expand list fields into individual values.
            if isinstance(value, list):
                parts.extend([str(v) for v in value if v is not None])
            # Keep scalar non-null values.
            elif value is not None:
                parts.append(str(value))
        # Join and normalize for consistent matching behavior.
        return self._normalize_text(" ".join(parts))

    # Select source subsets relevant to the user's question.
    def _select_relevant_records(self, user_input, history=None, max_schools=4):
        """
        Very simple retrieval:
        - always include district facts
        - include matching grade/program rules
        - include top matching school records
        """
        # Build token set used to score rule/school relevance.
        query_terms = self._extract_query_terms(user_input, history)

        # District facts are always included as baseline context.
        selected_district = DISTRICT_FACTS

        # Collect grade rules that contain at least one query token.
        selected_grade_rules = []
        for rule in GRADE_RULES:
            rule_text = self._record_to_text(rule)
            if any(term in rule_text for term in query_terms):
                selected_grade_rules.append(rule)

        # Collect program rules that contain at least one query token.
        selected_program_rules = []
        for rule in PROGRAM_RULES:
            rule_text = self._record_to_text(rule)
            if any(term in rule_text for term in query_terms):
                selected_program_rules.append(rule)

        # Score each school by number of matching query terms.
        school_scored = []
        for school in SCHOOL_RECORDS:
            school_text = self._record_to_text(school)
            score = sum(1 for term in query_terms if term in school_text)
            if score > 0:
                school_scored.append((score, school))

        # Rank schools highest-to-lowest by relevance score.
        school_scored.sort(key=lambda x: x[0], reverse=True)
        # Keep only the top-N matching schools.
        selected_schools = [school for _, school in school_scored[:max_schools]]

        # Return all selected source buckets.
        return selected_district, selected_grade_rules, selected_program_rules, selected_schools

    # Render selected sources into plain text for a system message.
    def _build_source_context(self, user_input, history=None):
        # Run retrieval to get relevant source records.
        district, grade_rules, program_rules, schools = self._select_relevant_records(user_input, history)

        # Build line-by-line context block.
        lines = []
        lines.append("BPS SOURCE INFORMATION")
        lines.append("")

        # Add district-wide facts section.
        if district:
            lines.append("District-wide facts:")
            for item in district:
                lines.append(f"- Fact: {item.get('fact')}")
                if item.get("notes"):
                    lines.append(f"  Notes: {item.get('notes')}")
                if item.get("sources"):
                    lines.append(f"  Sources: {'; '.join(item['sources'])}")
            lines.append("")

        # Add grade-rule section only when matches were found.
        if grade_rules:
            lines.append("Grade-specific rules:")
            for item in grade_rules:
                lines.append(f"- Fact: {item.get('fact')}")
                if item.get("notes"):
                    lines.append(f"  Notes: {item.get('notes')}")
                if item.get("sources"):
                    lines.append(f"  Sources: {'; '.join(item['sources'])}")
            lines.append("")

        # Add program-rule section only when matches were found.
        if program_rules:
            lines.append("Program-specific rules:")
            for item in program_rules:
                lines.append(f"- Fact: {item.get('fact')}")
                if item.get("notes"):
                    lines.append(f"  Notes: {item.get('notes')}")
                if item.get("sources"):
                    lines.append(f"  Sources: {'; '.join(item['sources'])}")
            lines.append("")

        # Add matching school records, if any.
        if schools:
            lines.append("Relevant school records:")
            for school in schools:
                lines.append(f"- School: {school.get('name')}")
                if school.get("neighborhood"):
                    lines.append(f"  Neighborhood: {school.get('neighborhood')}")
                if school.get("grades_served_text"):
                    lines.append(f"  Grades served: {school.get('grades_served_text')}")
                if school.get("school_type"):
                    lines.append(f"  School type: {', '.join(school.get('school_type', []))}")
                if school.get("program_tags"):
                    lines.append(f"  Program tags: {', '.join(school.get('program_tags', []))}")
                if school.get("language_programs"):
                    lines.append(f"  Language programs: {', '.join(school.get('language_programs', []))}")
                if school.get("special_features"):
                    lines.append(f"  Special features: {', '.join(school.get('special_features', []))}")
                if school.get("notes"):
                    lines.append(f"  Notes: {school.get('notes')}")
                if school.get("sources"):
                    lines.append(f"  Sources: {'; '.join(school['sources'])}")
            lines.append("")
        else:
            # Explicitly state when school matching found no results.
            lines.append("Relevant school records:")
            lines.append("- No specific school records matched the current question.")
            lines.append("")

        # Return one multi-line source context block.
        return "\n".join(lines)

    # Build model-ready message list with instructions, sources, history, and user query.
    def format_prompt(self, user_input, history=None):
        """        
        This method should:
        1. Add any necessary system context or instructions
        2. Format the user's input appropriately
        3. Add any special tokens or formatting the model expects

        Updated implementation: 
        Build chat messages for the model:
        1. behavior instructions
        2. retrieved BPS source information
        3. prior conversation history
        4. latest user message

        Args:
            user_input (str): The user's question

        Returns:
            str: A formatted prompt ready for the model
        
        Example prompt format:
            "You are a helpful assistant that specializes in...
             User: {user_input}
             Assistant:"
        """
        # Build dynamic source block tailored to current query and recent history.
        source_context = self._build_source_context(user_input, history)

        # Start messages with strict behavior instructions plus retrieved source data.
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "system",
                "content": (
                    #"Use only the following source information when answering.\n\n"
                    "Use this source information for reference when answering the user's question.\n\n"
                    f"{source_context}"
                ),
            },
        ]

        # Merge conversation history when present, supporting multiple history formats.
        if history:
            # Peek at first item to infer likely history schema.
            first = None
            try:
                first = history[0]
            except Exception:
                first = None

            # If history already uses OpenAI-style role/content dicts, append directly.
            if isinstance(first, dict) and "role" in first and "content" in first:
                messages.extend(history)
            else:
                # Otherwise normalize list/tuple/dict variants into role/content messages.
                for item in history:
                    if isinstance(item, (list, tuple)):
                        if len(item) >= 2:
                            user_msg, bot_msg = item[0], item[1]
                            messages.append({"role": "user", "content": str(user_msg)})
                            messages.append({"role": "assistant", "content": str(bot_msg)})
                    elif isinstance(item, dict):
                        if "user" in item and "assistant" in item:
                            messages.append({"role": "user", "content": str(item["user"])})
                            messages.append({"role": "assistant", "content": str(item["assistant"])})
                        elif "role" in item and "content" in item:
                            messages.append(
                                {"role": item["role"], "content": str(item["content"])}
                            )

        # Add the latest user question as the final message in the sequence.
        messages.append({"role": "user", "content": user_input})
        # Return fully assembled message list for generation.
        print(messages)
        return messages

    # Generate a model response from user input and optional history.
    def get_response(self, user_input, history=None):
        """
        TODO: Implement this method to generate responses to user questions.
        
        This method should:
        1. Use format_prompt() to prepare the input
        2. Generate a response using the model
        3. Clean up and return the response

        Args:
            user_input (str): The user's question

        Returns:
            str: The chatbot's response

        Implementation tips:
        - Use self.format_prompt() to format the user's input
        - Use self.client to generate responses
        """
        # step 1 - format messages
        # Build inference-ready chat messages.
        messages = self.format_prompt(user_input, history)

        # step 2 - generate response (with error handling and lower temperature to avoid halucinations)
        try:
            # Request a completion from the selected Hugging Face chat model.
            response = self.client.chat_completion(
                messages=messages,
                max_tokens=5000,
                temperature=0.4,  # lower temperature for more factual responses
            )
            # Return assistant text from first choice.
            return response.choices[0].message.content
        except Exception as e:
            # Return user-friendly error fallback including diagnostic text.
            return (
                "I'm sorry — I ran into an issue generating a response just now. "
                "Please try again. "
                f"(Error: {str(e)})"
            )
