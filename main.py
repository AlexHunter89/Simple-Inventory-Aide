from modules.user import feature_coming_soon, greet_and_identify_user, warn_user_new_session, user_change_bin, get_admin_password
from modules.menu import display_menu
from modules.inventory import item_found_sequence, item_not_found_sequence, get_upc, get_existing_upc_data
from modules.data_manager import start_new_inventory_session, save_entry_log, load_inventory_session, save_inventory_log, bin_variable_file_handler, bin_changer, bin_reset
import sys
from rich import print
from rich.markup import escape

def main():
    user_identity = greet_and_identify_user()
    current_bin = bin_variable_file_handler()
    print(f"The current bin is: {escape(current_bin)}")
    while True:
        print(f"Current User: [blue]{escape(user_identity)}[/blue]")
        user_menu_entry = display_menu()
        if user_menu_entry == 'Start New Session (Not Recommended)':
            user_new_session_warning_response = warn_user_new_session()
            if user_new_session_warning_response == 'yes':
                password_result = get_admin_password()
                if not password_result:
                    print()
                    print("[bold red]Access Denied[/bold red]")
                    print()
                    continue
                print()
                print("[green]*New Session Started*[/green]")
                df = start_new_inventory_session()
                bin_reset()
                current_bin = bin_variable_file_handler()
                while True:
                    upc = str(get_upc())
                    if upc != '':
                        description, price = get_existing_upc_data(upc, df)                        
                        if description == None:
                            item_not_found_sequence(df, upc, user_identity, current_bin)
                        else:
                            item_found_sequence(df, description, upc, price, user_identity, current_bin)
                    else:
                        save_entry_log(df)
                        save_inventory_log(df)
                        break
            else:
                continue
        elif user_menu_entry == 'Load Previous Session (Recommended)':
            print()
            print("[green]*Previous Session Loaded*[/green]")
            df = load_inventory_session()
            while True:
                    upc = str(get_upc())
                    if upc != '':
                        description, price = get_existing_upc_data(upc, df)                        
                        if description == None:
                            item_not_found_sequence(df, upc, user_identity, current_bin)
                        else:
                            item_found_sequence(df, description, upc, price, user_identity, current_bin)
                    else:
                        save_entry_log(df)
                        save_inventory_log(df)
                        break
            else:
                continue
        elif user_menu_entry == 'Delete Entry':
            feature_coming_soon()
            continue
        elif user_menu_entry == 'Modify Entry':
            feature_coming_soon()
            continue
        elif user_menu_entry == 'Change Current Bin':
            print()
            print(f"Current Bin is: {current_bin}")
            user_change_bin_response = user_change_bin()
            if user_change_bin_response == 'yes':
                bin_changer()
                current_bin = bin_variable_file_handler()
            else:
                continue
        elif user_menu_entry == 'Exit':
            print()
            print("Thank you for using the Inventory System...")
            sys.exit()


if __name__ == "__main__":
    main()