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

menu_options = [
    'Start New Session (Not Recommended)',
    'Load Previous Session (Recommended)',
    'Delete Entry',
    'Modify Entry',
    'Change Current Bin',
    'Exit'
    ]

def display_menu(user_identity, current_bin):
    """
    Displays the main menu and prompts the user to select an action.

    Parameters:
        user_identity (str): The name or identifier of the current user.
        current_bin (str): The current active bin, which provides context for user operations.

    Returns:
        str: The user's selected menu option from the available choices.

    This function displays the current user identity and active bin, followed by a numbered list
    of menu options. The user selects an option, and the chosen option is returned as a string.
    """
    print(f"Current User: [blue]{escape(user_identity)}[/blue]")
    print(f"The current bin is: {escape(current_bin)}")
    user_menu_entry = pyip.inputMenu(menu_options, numbered=True)
    return user_menu_entry