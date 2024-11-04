from modules.user import feature_coming_soon, greet_and_identify_user, new_session_warning_sequence, user_change_bin
from modules.menu import display_menu
from modules.inventory import item_found_sequence, item_not_found_sequence, get_upc, get_existing_upc_data
from modules.data_manager import start_new_inventory_session, save_entry_log, load_inventory_session, save_inventory_log, bin_variable_file_handler, bin_changer, bin_reset
import sys
from rich import print

def main():
    # This greets the user and ask for their identity
    user_identity = greet_and_identify_user()

    # This will check to see if there is a bin variable text file
    # It displays the bin that was loaded or created
    current_bin = bin_variable_file_handler()

    # Main loop
    while True:
        # Prints user information and displays the menu
        user_menu_entry = display_menu(user_identity, current_bin)

        # If the user wants to start a new session
        if user_menu_entry == 'Start New Session (Not Recommended)':
            # Sends a warning to the user
            user_new_session_warning_response = new_session_warning_sequence()

            if user_new_session_warning_response:
                # If the user confirms a new session
                # This creates a new emtpy DataFrame
                df = start_new_inventory_session()
                # Resets the bin variable to default '1'
                current_bin = bin_reset()

                while True:
                    # Gets a UPC from the user. Converts it to a string with str() for parsing
                    upc = get_upc(df, user_identity, current_bin)
                    # If the UPC is a blank entry the user will return to the main menu
                    if upc == '':
                        break
            else:
                continue

        elif user_menu_entry == 'Load Previous Session (Recommended)':
            # Loads the previous Excel file to continue work
            df = load_inventory_session()

            while True:
                # Gets a UPC from the user. Converts it to a string with str() for parsing
                upc = str(get_upc(df, user_identity, current_bin))
                # If the UPC is a blank entry the user will return to the main menu
                if upc == '':
                    break

        elif user_menu_entry == 'Delete Entry':
            feature_coming_soon()
            continue

        elif user_menu_entry == 'Modify Entry':
            feature_coming_soon()
            continue

        elif user_menu_entry == 'Change Current Bin':
            print(f"\nCurrent Bin is: {current_bin}")
            user_change_bin_response = user_change_bin()

            if user_change_bin_response == 'yes':
                bin_changer()
                current_bin = bin_variable_file_handler()

            else:
                continue

        elif user_menu_entry == 'Exit':
            print("\nThank you for using the Inventory System...")
            sys.exit()


if __name__ == "__main__":
    main()