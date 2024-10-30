import pyinputplus as pyip

def display_menu():
    user_menu_entry = pyip.inputMenu(['Start New Session (Not Recommended)',
                                      'Load Previous Session (Recommended)',
                                      'Delete Entry',
                                      'Modify Entry',
                                      'Change Current Bin',
                                      'Exit'], numbered=True)
    return user_menu_entry