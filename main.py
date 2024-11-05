from modules.user import feature_coming_soon, greet_and_identify_user, new_session_warning_sequence, user_change_bin
from modules.menu import display_menu
from modules.inventory import get_upc
from modules.data_manager import start_new_inventory_session, save_entry_log, load_inventory_session, save_inventory_log, bin_variable_file_handler, bin_changer, bin_reset
import sys
from rich import print

def main():
    user_identity = greet_and_identify_user()   # Greets user and returns their 'identity'
    current_bin = bin_variable_file_handler()   # Loads previous bin or sets to '1' and returns the 'bin_variable'
    df = load_inventory_session()   # Load or create inventory DataFrame at the start

    while True: # Main loop
        user_menu_entry = display_menu(user_identity, current_bin) # Display main menu

        if user_menu_entry == 'Start New Session (Not Recommended)':
            user_new_session_warning_response = new_session_warning_sequence()  # Sends a warning to the user

            if user_new_session_warning_response:
                df = start_new_inventory_session()  # Create a new inventory DataFrame, overwriting any previous data
                current_bin = bin_reset() # Resets the bin variable to the default '1'

                while True:
                    # Gets a UPC from the user. Converts it to a string with str() for parsing
                    upc, df = get_upc(df, user_identity, current_bin)
                    # If the UPC is a blank entry the user will return to the main menu
                    if upc == '':
                        save_entry_log(df)
                        save_inventory_log(df)
                        break
            else:
                continue

        elif user_menu_entry == 'Load Previous Session (Recommended)':
            while True:
                # Gets a UPC from the user. Converts it to a string with str() for parsing
                upc, df = str(get_upc(df, user_identity, current_bin))
                # If the UPC is a blank entry the user will return to the main menu
                if upc == '':
                    save_entry_log(df)
                    save_inventory_log(df)
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
                new_bin = bin_changer()
                if new_bin:
                    current_bin = new_bin

            else:
                print("[yellow]Bin change cancelled. Returning to the main menu.[/yellow]")
                continue

        elif user_menu_entry == 'Exit':
            print("\nThank you for using the Inventory System...")
            sys.exit()


if __name__ == "__main__":
    main()