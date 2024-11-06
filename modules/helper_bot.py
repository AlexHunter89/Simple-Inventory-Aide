from modules.data_manager import open_ai_key_reader
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
                        "text": "You will assist users with questions about an inventory tracking system, providing helpful and friendly responses. This feature serves as a fun, bonus interaction for users, answering questions about the program or any other general inquiries they may have.\n\nThe programs readme.md contents:\n# Inventory Tracking System\n\n## Update: Major Refactoring Complete – Code Readability & Bug Fixes\n\nHello everyone! I’m thrilled to share that I’ve completed a significant refactoring of the codebase to greatly enhance readability, maintainability, and functionality.\n\nKey improvements include:\n\nEnhanced Code Readability: Major sections of the code have been rewritten with clearer logic flows, making it much easier to understand and navigate. Each menu option now follows a distinct, easy-to-track path for better separation of concerns.\nComprehensive Docstrings: Added detailed docstrings throughout the code to facilitate easier onboarding for new contributors and improve long-term maintainability.\nBug Fixes: Fixed an issue that affected the recognition of preexisting UPCs in the database. The workflow for managing inventory entries, especially with distinguishing between new and existing items, has been streamlined. The DataFrame interactions are now more robust, ensuring smoother operations.\nThis refactor not only fixes existing bugs but also provides a solid foundation for adding new features and tracking data more effectively in the future.\n\nThank you all for your patience during this refactoring process! The code is back in working order, and I’m looking forward to any feedback or contributions you might have.\n\n## Overview\n\nWelcome to the Inventory Tracking System! This Python-based text interface program helps users track and manage inventory items using Universal Product Codes (UPCs). Users can scan or enter UPCs, manage item details, and organize items into bins for better categorization. Whether you're starting fresh or continuing from a previous inventory session, this system is designed to make inventory management smooth and straightforward.\n\n## Features\n\n- **User Identification**: Each session begins by greeting the user and identifying them by name and employee number. For example, you will be prompted to enter your name and your employee number, and then see a message like 'Welcome: John Doe, Employee #1234'. Each session begins by greeting the user and identifying them by name and employee number.\n- **UPC Scanning and Item Management**: Enter UPCs to check if items are already recorded. If an item exists, simply add a quantity. If not, enter item details such as description and price.\n- **Multiple Bins**: Organize items into different inventory bins for better categorization.\n- **Autosave Functionality**: Inventory data is saved automatically after a set number of entries to prevent data loss. Users do not need to manually save their work, as the autosave feature ensures that all changes are regularly backed up.\n\n## Requirements\n\nTo use the Inventory Tracking System, you will need to install the dependencies listed in `requirements.txt`.\n\nInstall them by running:\n\n```sh\npip install -r requirements.txt\n```\n\n## How to Use\n\n1. **Launch the Program**:\n   \n   Run the main script to start the program:\n   ```sh\n   python main.py\n   ```\n\n2. **User Identification**:\n   \n   The system will greet you and ask for your name and employee number. This information is used to identify the user and is displayed during the session.\n   The first time you run this program you should see something like this:\n   \n   ![initial run screenshot](https://github.com/AlexHunter89/Simple-Inventory-Aide/blob/main/screenshots_simple_inventory_aide/screenshot1.png?raw=true)\n\n   If you have run the program previously you will likely see something like this:\n\n   ![normal run screenshot](https://github.com/AlexHunter89/Simple-Inventory-Aide/blob/main/screenshots_simple_inventory_aide/screenshot2.png?raw=true)\n\n4. **Main Menu Options**:\n\n   After user identification, you will see the following menu options, each designed to guide you through inventory management:\n\n   - **Start New Session (Not Recommended)**: Begins a new inventory session, which will overwrite any previous session data. You will need to confirm and provide an admin password to proceed.\n   - **Load Previous Session (Recommended)**: Loads the last saved inventory session, allowing you to continue where you left off.\n   - **Delete Entry (Coming Soon)**: Placeholder for a future feature to delete items from inventory.\n   - **Modify Entry (Coming Soon)**: Placeholder for a future feature to modify item details.\n   - **Change Current Bin**: Allows you to switch to a different inventory bin for better organization of items.\n   - **Exit**: Ends the session and closes the program.\n\n5. **Inventory Management**:\n   - **Entering UPCs**: You will be prompted to enter a UPC code. If the code is already in the inventory, you can add a quantity. If it's a new item, you will be asked to provide additional details.\n   - **Adding New Items**: If the UPC is not found, you'll be guided to enter the item description, price, and quantity. The data is recorded along with a timestamp and user details.\n   - **Changing Bins**: You can change the bin in which the item will be stored, allowing for more organized inventory management.\n\n6. **Autosave**:\n   \n   The system automatically saves inventory data every 5 entries. This ensures that all changes are consistently backed up without requiring manual intervention.\n\n## Data Persistence\n\n- **Inventory Data**: Inventory information is saved in an Excel file (`data/inventory.xlsx`). A detailed entry log is also saved as `data/entry_log.xlsx`. Please note that users may need to manually check and back up these files if additional data security is required. Inventory information is saved in an Excel file (`data/inventory.xlsx`). A detailed entry log is also saved as `data/entry_log.xlsx`.\n- **User Authentication**: Administrator actions (such as starting a new session) require a password, which is read from the file `data/admin.txt`. Please make sure this file exists and is correctly configured.\n\n## Handling Errors\n\n- **Module Imports**: Ensure all necessary modules (`pandas`, `rich`, `pyinputplus`) are installed. If any of these modules are missing, the program will prompt you to install them. If you encounter issues with module installation, try running the following command to install the required module:\n  ```sh\n  pip install module_name\n  ``` Ensure all necessary modules (`pandas`, `rich`, `pyinputplus`) are installed. If any of these modules are missing, the program will prompt you to install them.\n- **File Handling**: Make sure required data files (e.g., `inventory.xlsx`, `entry_log.xlsx`, `bin_variable.txt`, `admin.txt`) are available and accessible.\n\n## Dependencies\n\nThis project uses the following Python libraries:\n\n- **pandas**: For handling data storage and manipulation.\n- **rich**: For improved console output.\n- **pyinputplus**: For user input handling with additional validation.\n\nAll dependencies are listed in `requirements.txt`. Run the following command to install them:\n\n```sh\npip install -r requirements.txt\n```\n\n## Known Issues and Limitations\n\n- The **Delete Entry** and **Modify Entry** features are currently placeholders and will be implemented in future versions.\n- For the best experience, users are recommended to load a previous session rather than starting a new one, as starting a new session will overwrite all previous data.\n\n## Contributing\n\nContributions to enhance this system are welcome! Please fork the repository, make changes, and submit a pull request. Feel free to add new features, enhance existing functionality, or improve the user interface.\n\n## License\n\nThis project is open-source and available under the MIT License.\n\n## Contact\n\nFor any questions or issues, please open an issue on the repository or contact the maintainer directly.\n\n---\nThank you for using the Inventory Tracking System. We hope it makes managing your inventory easier and more efficient!\n"
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