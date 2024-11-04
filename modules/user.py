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
        - The password is read from a file named `password.txt`. Ensure this file exists and contains 
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
    change_bin_prompt = "\nWould you like to change the current bin you are working on? (yes/no): "
    change_bin_response = pyip.inputYesNo(prompt=change_bin_prompt)
    return change_bin_response

    
def feature_coming_soon():
    print("\n[blue]Feature coming soon![/blue]\n")
