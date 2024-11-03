import pyinputplus as pyip

def display_menu():
    """Displays the main menu. It shows all of the available actions that the user can take."""
    user_menu_entry = pyip.inputMenu(['Start New Session (Not Recommended)',
                                      'Load Previous Session (Recommended)',
                                      'Delete Entry',
                                      'Modify Entry',
                                      'Change Current Bin',
                                      'Exit'], numbered=True)
    return user_menu_entry