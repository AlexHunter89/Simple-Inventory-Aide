from modules.data_manager import read_password_from_file

try:
    import pyinputplus as pyip
except ImportError:
    print("Error: The module 'pyinputplus' is not installed.")
    print("Please install it by running: python -m pip install pyinputplus")
    exit(1)

try:
    from rich import print
    from rich.markup import escape
except ImportError:
    print("Error: The module 'rich' is not installed.")
    print("Please install it by running: python -m pip install rich")
    exit(1)

def greet_and_identify_user():
    """
    Greets the user and captures their name and employee number.

    Prompts the user to input their name and employee number, both of which are required
    for identification purposes. The employee number must be an integer, but the values 
    are not validated against an external database.

    Returns:
        str: A concatenated string combining the user's name and employee number in the format
        'user_name: employee_number', used to track the current user.   
    """
    print("\nWelcome to the inventory tracking system.\n")
    user_name_prompt = "Please enter your name: "
    user_name = pyip.inputStr(prompt=user_name_prompt, strip=True)
    employee_number_prompt = "Please enter your employee number: "
    employee_number = pyip.inputNum(prompt=employee_number_prompt, min=0, strip=True)
    user_identity = f"{escape(user_name)}: {employee_number}"
    print(f"\nWelcome: {escape(user_name)}")
    return user_identity

def new_session_warning_sequence():
    """
    Warns the user about data overwrite risks when starting a new session and prompts for confirmation.

    This function is called when the user attempts to start a new inventory session. It first warns the 
    user that starting a new session will overwrite all previous session data. The user must confirm 
    if they want to continue, and if confirmed, they must enter an administrator password. The password 
    is read from an external text file (`admin.txt`). If the user declines or the password is incorrect, 
    the function will not allow the new session to start.

    Parameters:
        None

    Returns:
        bool: 
            - Returns True if the user confirms the warning and enters the correct password.
            - Returns False if the user declines to continue, the password file cannot be read, or if the password is incorrect.
        
    Notes:
        - The password is read from a file named `admin.txt`. Ensure this file exists and contains 
          the correct password.
        - For demonstration purposes, this approach is used to keep things simple, but for production use, 
          stronger security measures should be implemented, such as using environment variables or secure vaults.
    """
    new_session_overwrite_warning = "\n[bold red]WARNING![/bold red] Starting a new session will overwrite any previous sessions.\n"
    print(new_session_overwrite_warning)

    user_continuation_prompt = "Are you sure you want to continue? (yes/no): "    
    user_continuation_response = pyip.inputYesNo(prompt=user_continuation_prompt)
    print()

    if user_continuation_response == 'no':
        print("[yellow]New session canceled. Returning to the main menu.[/yellow]\n")
        return False
    
    new_session_overwrite_warning_2 = "\nPlease note that continuing will overwrite any previous data.\n"
    print(new_session_overwrite_warning_2)

    password = read_password_from_file()
    if not password:
        print("[red]Password could not be retrieved. Aborting action.[/red]")
        return False
    
    password_prompt = "Please enter the password: "
    user_password_response = pyip.inputPassword(prompt=password_prompt)

    if user_password_response == password:
        print("\n[green]*New Session Started*[/green]")
        return True
    else:
        print("\n[bold red]Access Denied[/bold red] [yellow]Returning to the main menu.[/yellow]\n")
        return False

def user_change_bin():
    """
    Prompts the user to confirm if they want to change the current bin.

    This function presents a yes/no prompt to the user asking if they wish to change the current
    bin they are working on. It returns the user's response.

    Parameters:
        None

    Returns:
        str: The user's response ('yes' or 'no') to the change bin prompt.
    """
    default_answer = 'no'
    change_bin_prompt = "\nWould you like to change the current bin you are working on? (yes/no): "
    change_bin_response = pyip.inputYesNo(prompt=change_bin_prompt, default=default_answer)
    return change_bin_response

def feature_coming_soon():
    print("\n[blue]Feature coming soon![/blue]\n")

def get_user_upc_input():
    """
    Prompts the user for a UPC code and returns the value.
    
    Returns:
        str: The UPC code inputted by the user or an empty string if the user wishes to return.
    """
    upc_entry_prompt = "\nPlease enter a UPC code (Or press Enter to save and return to the Main Menu): "
    upc = pyip.inputNum(prompt=upc_entry_prompt, blank=True)
    return str(upc)

def get_item_details():
    """
    Prompt the user for item description and price.
    
    Returns:
        tuple: (description, price) provided by the user. The description is a non-empty string,
        and the price is a positive number.
        
    Raises:
        ValueError: If the price entered is not a positive number.
    """    
    description_entry_prompt = "Please enter the item description (or press Enter to cancel): " # Prompt for description
    description = pyip.inputStr(prompt=description_entry_prompt)
    
    if description.strip() == '':
        print("No description entered. Cancelling item entry.")
        return None, None  # Return to indicate no valid item was added.
    
    while True: # Prompt for price
        price_entry_prompt = "Please enter the item price (must be positive): "
        price = pyip.inputNum(prompt=price_entry_prompt)
        
        if price > 0:
            break
        else:
            print("Invalid price. Price must be greater than zero. Please try again.")

    return description, price

def get_quantity():
    """
    Prompt the user for quantity of items.
    
    Returns:
        int: The quantity entered by the user. A value of 0 indicates no update to quantity.
    """
    quantity_entry_prompt = (
        "Please enter the item quantity (Enter 0 to cancel adding/updating the item quantity): "
    )
    quantity = pyip.inputNum(prompt=quantity_entry_prompt, min=0)
    
    if quantity == 0:
        print("Quantity set to 0. No quantity will be added for this item.")
    
    return quantity

def chat_gpt_greeting():
    question_prompt = "\nWhat can I help you with?\n"
    user_question = pyip.inputStr(prompt=question_prompt)
    return user_question