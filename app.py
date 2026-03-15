"""
Gradio Web Interface for Boston School Chatbot

This script creates a web interface for your chatbot using Gradio.
You only need to implement the chat function.

Key Features:
- Creates a web UI for your chatbot
- Handles conversation history
- Provides example questions
- Can be deployed to Hugging Face Spaces

Example Usage:
    # Run locally:
    python app.py
    
    # Access in browser:
    # http://localhost:7860
"""

import gradio as gr
from src.chat import Chatbot

def create_chatbot():
    """
    Creates and configures the chatbot interface.
    """
    chatbot = Chatbot()
    
    def chat(message, history):
        """
        TODO:Generate a response for the current message in a Gradio chat interface.
        
        This function is called by Gradio's ChatInterface every time a user sends a message.
        You only need to generate and return the assistant's response - Gradio handles the
        chat display and history management automatically.

        Args:
            message (str): The current message from the user
            history (list): List of previous message pairs, where each pair is
                           [user_message, assistant_message]
                           Example:
                           [
                               ["What schools offer Spanish?", "The Hernandez School..."],
                               ["Where is it located?", "The Hernandez School is in Roxbury..."]
                           ]

        Returns:
            str: The assistant's response to the current message.


        Note:
            - Gradio automatically:
                - Displays the user's message
                - Displays your returned response
                - Updates the chat history
                - Maintains the chat interface
            - You only need to:
                - Generate an appropriate response to the current message
                - Return that response as a string
        """
        # TODONE: Generate and return response
        return chatbot.get_response(message, history)

    
    
    # Create Gradio interface. Customize the interface however you'd like (ie. make more accessible, user friendly, etc)
    # ensure that we document any changes in the memo
    demo = gr.ChatInterface(
        chat,
        title="Boston Publice Schools Chatbot",
        description=
        """
        Ask me anything about Boston Public Schools! Since I am a free tier chatbot, 
        I may give a 503 error when I'm busy. If that happens, please try again a few seconds later. 
        Lets start by establishing which language you speak! I can understand and respond in multiple languages, 
        so feel free to ask your question in the language you're most comfortable with.
        """,

        # TODONE: Multilingual support.
        examples=[
            "English: I speak English",
            "Spanish: Yo hablo español",
            "Portuguese: Eu falo português",
            "Chinese: 我会说中文 (Wǒ huì shuō zhōngwén)",
            "Haitian Creole: Mwen pale kreyòl ayisyen",
            "French: Je parle français",
            "Vietnamese: Tôi nói tiếng Việt",
            "Arabic: أنا أتكلم العربية (Ana atakallam al-ʿarabiyya)",
            "Russian: Я говорю по-русски (Ya govoryu po-russki)",
            "Somali: Waxaan ku hadlaa af Soomaali",
            "Kabuverdianu: N ta papia kabuverdianu",
            "Hindi: मैं हिंदी बोलता हूँ (Main Hindi bolta hoon)",
            "Korean: 저는 한국어를 말합니다 (Jeoneun hangugeo-reul malhabnida)",
        ]
    )
    
    return demo

if __name__ == "__main__":
    demo = create_chatbot()
    demo.launch()
