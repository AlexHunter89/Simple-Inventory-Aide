import pyinputplus as pyip
from rich import print
from rich.markup import escape

def display_menu(user_identity, current_bin):
    """Displays the main menu. It shows all of the available actions that the user can take.
    Also displays the current active user."""
    print(f"Current User: [blue]{escape(user_identity)}[/blue]")
    print(f"The current bin is: {escape(current_bin)}")
    user_menu_entry = pyip.inputMenu(['Start New Session (Not Recommended)',
                                      'Load Previous Session (Recommended)',
                                      'Delete Entry',
                                      'Modify Entry',
                                      'Change Current Bin',
                                      'Exit'], numbered=True)
    return user_menu_entry