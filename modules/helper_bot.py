from modules.data_manager import open_ai_key_reader, read_assistant_prompt
from modules.user import chat_gpt_question_prompt

try:
    from rich import print
    from rich.markup import escape
except ImportError:
    print("Error: The module 'rich' is not installed.")
    print("Please install it by running: python -m pip install rich")
    exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("Error: The module 'openai' is not installed.")
    print("Please install it by running: python -m pip install openai")
    exit(1)

try:
    import pyinputplus as pyip
except ImportError:
    print("Error: The module 'pyinputplus' is not installed.")
    print("Please install it by running: python -m pip install pyinputplus")
    exit(1)

def open_ai_helper_bot():
    """
    Initializes and manages an interactive chat session with an AI assistant powered by the OpenAI API.

    This function performs the following sequence of operations:
    1. Reads an API key for OpenAI using the `open_ai_key_reader` helper function. 
       If the key is unavailable or invalid, an error message is displayed, and the function exits.
    2. Instantiates an OpenAI client using the provided API key, allowing the bot to communicate with OpenAI's API.
    3. Welcomes the user with an introductory message, explaining the bot's primary purpose and general functionality.
    4. Enters an interactive loop where it:
       - Prompts the user for input via `chat_gpt_question_prompt`, which asks for a question or command.
       - Sends the user's query to the OpenAI API and retrieves a response.
       - Displays the response, formatted for readability.
       - Terminates the loop and ends the session if the user inputs 'quit'.
    5. Returns `True` to signify successful execution of the session.

    Returns:
        bool: True if the function executes successfully, allowing the bot to run an interactive session. 
              This return value serves as an indicator of successful session completion.

    Notes:
        - This function assumes the existence of a helper function `open_ai_key_reader()` to fetch the API key.
        - The `chat_gpt_question_prompt()` helper function is used to manage user prompts.
        - The function continuously runs until the user types 'quit' to exit the session.
    """
    key = open_ai_key_reader()
    system_prompt = read_assistant_prompt()

    if key != None:
        client = OpenAI(api_key=key)    # Finds the API key

        # Greets the user and explains the expected interactions
        print("""
              Welcome to the AI help system.
              
              This bot is built to assistant you in using the inventory tracking system.
              However, it is a general use chat bot and it will technically converse about anything.
              Feel free to ask the bot about whatever comes to your mind!
              """)



        while True:
            user_question = chat_gpt_question_prompt()

            if user_question == 'quit':
                break

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                    "role": "system",
                    "content": [
                        {
                        "type": "text",
                        "text": system_prompt
                        }
                    ]
                    },
                    {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": user_question
                        }
                    ]
                }],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={
                    "type": "text"
                }
                )

            print(f"[blue]{response.choices[0].message.content}[/blue]")

        return True
    return True