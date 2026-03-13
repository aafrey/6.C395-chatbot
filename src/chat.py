from huggingface_hub import InferenceClient
from config import BASE_MODEL, MY_MODEL, HF_TOKEN

# example system prompt
SYSTEM_PROMPT = """You are a helpful assistant that helps families in Boston find the right public school for their children. You have knowledge about Boston Public Schools, including:
 - School locations and neighborhoods
 - Grade leevels offered (K0, K1, K2, elementary, middle, high school)
 - Lanuague programs (dual language, ESL, sheltered English)
 - Special education services
 - Application and enrollment processes
 - Transportation and bus routes
 - After-school programs

When helping families:
 - Ask clarifying questions about their neighborhood, child's age, and preferences
 - Provide specific school recommendatiosn when possible
 - Be honest when you are unsure about specific details and direct them to bostonpublicschools.org
 - Be warm and supportive, choosing a school is a big decision for families
 - If the user asks questions unrelated to Boston Public Schools, politely redirect

Key facts:
 - Boston uses a home-based assignment system where families get a list of schools based on their address
 - Families can register at any Welcome Center or online
 - Registration typically opens in January for the following school year
 - The BPS website is bostonpublicschools.org
Example questions:
I live in Jamaica Plain and want to send my child to kindergarten. What schoools are available,
What language programs are offered in Boston Public Schools?,
How do I register my child for school?"""


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
        
    def format_prompt(self, user_input, history=None):
        """
        TODO: Implement this method to format the user's input into a proper prompt.
        Keep track of changes as we go and write about them in the memo!
        
        This method should:
        1. Add any necessary system context or instructions
        2. Format the user's input appropriately
        3. Add any special tokens or formatting the model expects

        Args:
            user_input (str): The user's question

        Returns:
            str: A formatted prompt ready for the model
        
        Example prompt format:
            "You are a helpful assistant that specializes in...
             User: {user_input}
             Assistant:"
        """
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if history:
            # AAF 2026-03-13: Updated to handle various types of message formats, fixes bug that occurred when second message was sent (history had 1 item instead of 2)
            first = None
            try:
                first = history[0]
            except Exception:
                first = None

            if isinstance(first, dict) and 'role' in first and 'content' in first:
                messages.extend(history)
            else:
                for item in history:
                    # pair-like: (user_msg, assistant_msg) or [user_msg, assistant_msg]
                    if isinstance(item, (list, tuple)):
                        if len(item) >= 2:
                            user_msg, bot_msg = item[0], item[1]
                            messages.append({"role": "user", "content": user_msg})
                            messages.append({"role": "assistant", "content": bot_msg})
                        else:
                            # unexpected short sequence; skip
                            continue
                    elif isinstance(item, dict):
                        # dict with explicit keys
                        if 'user' in item and 'assistant' in item:
                            messages.append({"role": "user", "content": item['user']})
                            messages.append({"role": "assistant", "content": item['assistant']})
                        elif 'role' in item and 'content' in item:
                            messages.append(item)
                        else:
                            # unknown dict shape; skip
                            continue
                    else:
                        # unknown item type; skip
                        continue
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
        print("DEBUG: get_response received history:", repr(history))
        print("DEBUG: user_msg:", history[0] if history else 0)
        print("DEBUG: bot_msg:", history[1] if history else 1)
        messages = self.format_prompt(user_input, history)

        # step 2 - generate response
        response = self.client.chat_completion(messages=messages)

        # step 3 - 
        return response.choices[0].message.content

