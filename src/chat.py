from huggingface_hub import InferenceClient
from config import BASE_MODEL, MY_MODEL, HF_TOKEN
from src.bps_data import DISTRICT_SOURCES, DISTRICT_FACTS, GRADE_RULES, PROGRAM_RULES, SCHOOL_RECORDS, SEI_LANGUAGE_SPECIFIC_EXAMPLES

# improved system prompt, which directs to bps_data, rather than including data directly here
SYSTEM_PROMPT = """You are a Boston Public Schools enrollment helper.

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
- Be warm, concise, and helpful.
- If the question is unrelated to Boston Public Schools, politely redirect.

Helpful guidance:
- Important details may include grade level, child age, home address or neighborhood, language preferences, and special program needs.
- Do not claim a school is definitely available unless the provided source information supports that.
"""

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
        model_id = MY_MODEL if MY_MODEL else BASE_MODEL # define MY_MODEL in config.py if you create a new model in the HuggingFace Hub
        self.client = InferenceClient(model=model_id, token=HF_TOKEN)

    def _normalize_text(self, text):
        return text.lower().strip() if text else ""

    def _extract_query_terms(self, user_input, history=None):
        """
        Build a small bag of query terms from the current user input and recent history.
        This is a lightweight retrieval helper, not full NLP.
        """
        combined = user_input or ""

        if history:
            for item in history[-3:]:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    combined += " " + str(item[0]) + " " + str(item[1])
                elif isinstance(item, dict):
                    combined += " " + str(item.get("content", ""))
                else:
                    combined += " " + str(item)

        text = self._normalize_text(combined)

        # basic synonym expansion
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

        expanded = text
        for key, value in replacements.items():
            if key in text:
                expanded += " " + value

        return set(expanded.split())

    def _record_to_text(self, record):
        """
        Flatten a record into searchable text.
        """
        parts = []
        for value in record.values():
            if isinstance(value, list):
                parts.extend([str(v) for v in value if v is not None])
            elif value is not None:
                parts.append(str(value))
        return self._normalize_text(" ".join(parts))

    def _select_relevant_records(self, user_input, history=None, max_schools=4):
        """
        Very simple retrieval:
        - always include district facts
        - include matching grade/program rules
        - include top matching school records
        """
        query_terms = self._extract_query_terms(user_input, history)

        selected_district = DISTRICT_FACTS

        selected_grade_rules = []
        for rule in GRADE_RULES:
            rule_text = self._record_to_text(rule)
            if any(term in rule_text for term in query_terms):
                selected_grade_rules.append(rule)

        selected_program_rules = []
        for rule in PROGRAM_RULES:
            rule_text = self._record_to_text(rule)
            if any(term in rule_text for term in query_terms):
                selected_program_rules.append(rule)

        school_scored = []
        for school in SCHOOL_RECORDS:
            school_text = self._record_to_text(school)
            score = sum(1 for term in query_terms if term in school_text)
            if score > 0:
                school_scored.append((score, school))

        school_scored.sort(key=lambda x: x[0], reverse=True)
        selected_schools = [school for _, school in school_scored[:max_schools]]

        return selected_district, selected_grade_rules, selected_program_rules, selected_schools

    def _build_source_context(self, user_input, history=None):
        district, grade_rules, program_rules, schools = self._select_relevant_records(user_input, history)

        lines = []
        lines.append("BPS SOURCE INFORMATION")
        lines.append("")

        if district:
            lines.append("District-wide facts:")
            for item in district:
                lines.append(f"- Fact: {item.get('fact')}")
                if item.get("notes"):
                    lines.append(f"  Notes: {item.get('notes')}")
                if item.get("sources"):
                    lines.append(f"  Sources: {'; '.join(item['sources'])}")
            lines.append("")

        if grade_rules:
            lines.append("Grade-specific rules:")
            for item in grade_rules:
                lines.append(f"- Fact: {item.get('fact')}")
                if item.get("notes"):
                    lines.append(f"  Notes: {item.get('notes')}")
                if item.get("sources"):
                    lines.append(f"  Sources: {'; '.join(item['sources'])}")
            lines.append("")

        if program_rules:
            lines.append("Program-specific rules:")
            for item in program_rules:
                lines.append(f"- Fact: {item.get('fact')}")
                if item.get("notes"):
                    lines.append(f"  Notes: {item.get('notes')}")
                if item.get("sources"):
                    lines.append(f"  Sources: {'; '.join(item['sources'])}")
            lines.append("")

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
            lines.append("Relevant school records:")
            lines.append("- No specific school records matched the current question.")
            lines.append("")

        return "\n".join(lines)

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
        source_context = self._build_source_context(user_input, history)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "system",
                "content": (
                    "Use only the following source information when answering.\n\n"
                    f"{source_context}"
                ),
            },
        ]

        if history:
            first = None
            try:
                first = history[0]
            except Exception:
                first = None

            if isinstance(first, dict) and "role" in first and "content" in first:
                messages.extend(history)
            else:
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

        messages.append({"role": "user", "content": user_input})
        return messages

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
        messages = self.format_prompt(user_input, history)

        # step 2 - generate response (with error handling and lower temperature to avoid halucinations)
        try:
            response = self.client.chat_completion(
                messages=messages,
                max_tokens=500,
                temperature=0.2,
            )
            return response.choices[0].message.content
        except Exception as e:
            return (
                "I'm sorry — I ran into an issue generating a response just now. "
                "Please try again. "
                f"(Error: {str(e)})"
            )
