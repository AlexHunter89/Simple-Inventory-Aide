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

            assistant = client.beta.assistants.create(
                name="Inventory Help Bot",
                instructions="You are a friendly and helpful assistant for the Inventory Tracking System. Users may come to you with questions about how to use the system or express confusion about certain features. While you have specialized knowledge about the program, feel free to interact with users about anything they wish to discuss. Your approach should be light-hearted and fun, making users feel like they're chatting with their best friend who just happens to be really smart. Use simple, clear language without dumbing things down. You have the tiniest bit of southern charm at times and at other times a bit of east coast grit. Give it personality but using unique phrases.",
                model="gpt-3.5-turbo",
                tools=[{"type": "file_search"}]
            )

            # Create a vector store caled "Financial Statements"
            vector_store = client.beta.vector_stores.create(name="Inventory Docs")
            
            # Ready the files for upload to OpenAI
            file_paths = ["readme.md", "main.py", "modules/data_manager.py", "modules/helper_bot.py", "modules/inventory.py", "modules/menu.py", "modules/user.py"]
            file_streams = [open(path, "rb") for path in file_paths]
            
            # Use the upload and poll SDK helper to upload the files, add them to the vector store,
            # and poll the status of the file batch for completion.
            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
            )
            
            # You can print the status and the file counts of the batch to see the result of this operation.
            # print(file_batch.status)
            # print(file_batch.file_counts)

            assistant = client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
            )
            
            # Create a thread and attach the file to the message
            thread = client.beta.threads.create(
            messages=[{
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": user_question
                        }
                    ]
                }])
            
            # The thread now has a vector store with that file in its tool resources.
            print(thread.tool_resources.file_search)

            from typing_extensions import override
            from openai import AssistantEventHandler, OpenAI
            
            client = OpenAI(api_key=key)
            
            class EventHandler(AssistantEventHandler):
                @override
                def on_text_created(self, text) -> None:
                    print(f"\nassistant > ", end="", flush=True)

                @override
                def on_tool_call_created(self, tool_call):
                    print(f"\nassistant > {tool_call.type}\n", flush=True)

                @override
                def on_message_done(self, message) -> None:
                    # print a citation to the file searched
                    message_content = message.content[0].text
                    annotations = message_content.annotations
                    citations = []
                    for index, annotation in enumerate(annotations):
                        message_content.value = message_content.value.replace(
                            annotation.text, f"[{index}]"
                        )
                        if file_citation := getattr(annotation, "file_citation", None):
                            cited_file = client.files.retrieve(file_citation.file_id)
                            citations.append(f"[{index}] {cited_file.filename}")

                    print(message_content.value)
                    print("\n".join(citations))


            # Then, we use the stream SDK helper
            # with the EventHandler class to create the Run
            # and stream the response.

            with client.beta.threads.runs.stream(
                thread_id=thread.id,
                assistant_id=assistant.id,
                instructions="Please address the user as Jane Doe. The user has a premium account.",
                event_handler=EventHandler(),
            ) as stream:
                stream.until_done()

            """
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

            print(f"[blue]{response.choices[0].message.content}[/blue]")"""

        return True
    return True