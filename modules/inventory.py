import pyinputplus as pyip
from datetime import datetime
from modules.data_manager import auto_save, save_entry_log, save_inventory_log
from modules.user import get_user_upc_input, get_item_details, get_quantity
from rich import print

def validate_upc(upc):
    """
    Validates the UPC code format.
    
    Args:
        upc (str): The UPC code entered by the user.
        
    Returns:
        bool: True if the UPC is valid, False otherwise.
    """
    if len(upc) != 12:
        print("Invalid UPC length. Please enter a 12-digit UPC code.")
        return False
    return True

def get_upc(df, user_identity, current_bin):
    """
    Asks the user to enter a UPC number and handles validation and subsequent item lookups.
    
    Args:
        df (DataFrame): The inventory DataFrame.
        user_identity (str): The identity of the user performing the operation.
        current_bin (str): The identifier for the current inventory bin.
        
    Returns:
        tuple: The UPC code (str) and the updated DataFrame.
    """
    while True:
        upc = get_user_upc_input()  # Step 1: Get the UPC from the user

        if upc == '':   # Step 2: Check if the user wants to return to the main menu
            break   # Return to main menu

        if not validate_upc(upc):   # Step 3: Validate the UPC length
            continue    # Invalid UPC, ask again

        description, price = get_existing_upc_data(upc, df) # Step 4: Look up the item in the inventory

        if description is None:
            # Item not found, call the appropriate sequence
            item_not_found_sequence(df, upc, user_identity, current_bin)
        else:
            # Item found, call the appropriate sequence
            item_found_sequence(df, description, upc, price, user_identity, current_bin)
        
        # Since we either find an item or not, we should break after the first valid UPC check
        return upc, df

    # If the loop ends without finding an item or breaking for valid reasons, return an empty UPC and df
    return '', df

def get_existing_upc_data(upc, df):
    """
    Searches for an existing UPC in the inventory DataFrame and retrieves its details.
    
    Args:
        upc (str): The UPC code to search for.
        df (DataFrame): The inventory DataFrame containing product information.
        
    Returns:
        tuple: (description, price) if found, otherwise (None, None).
    """
    try:
        matches = df[df['UPC'] == str(upc)] # Ensure UPC is treated as a string for matching consistency
        
        if not matches.empty:   # Check if there are any matches
            # Extract the first matching entry
            previous_entry = matches.iloc[0]
            description = previous_entry['Description']
            price = previous_entry['Price']
            return (description, price)
        
        return (None, None) # No match found
    except KeyError as e:
        # Handle case where 'UPC', 'Description', or 'Price' columns are missing
        print(f"Error: Missing column in DataFrame: {e}")
        return None, None
    except Exception as e:
        # General catch for any unexpected issues
        print(f"An unexpected error occurred: {e}")
        return None, None

def add_item(df, date_time, description, quantity, upc, price, user_identity, current_bin):
    new_item = {
        'DateTime': date_time,
        'Description': description,
        'Quantity': quantity,
        'UPC': upc,
        'Price': price,
        'User': user_identity,
        'Bin': current_bin
    }

    df.loc[len(df)] = new_item
    return df

def item_not_found_sequence(df,  upc, user_identity, current_bin):
    # Step 1: Notify the user that the item wasn't found
    item_details_needed_prompt = "\n[yellow]Could not find item in database. Please enter the details.[/yellow]\n"
    print(item_details_needed_prompt)

    description, price = get_item_details() # Step 2: Gather the new item details

    if description is None and price is None:
        print("No item added. Returning to main menu.")
        return None # If user cancels entry, stop further processing.

    quantity = get_quantity()   # Step 3: Gather quantity details

    if quantity == 0:
        print("No quantity added. Returning to main menu.")
        return None # Stop further processing if quantity is zero.

    date_time = datetime.now()  # Step 5: Get the current timestamp

    df = add_item(df, date_time, description, quantity, upc, price, user_identity, current_bin)
    auto_save(df)
    print()
    print(df.tail())
    return None

def item_found_sequence(df, description, upc, price, user_identity, current_bin):
    item_details_found_prompt = "Item found! Details extracted!"
    print()
    print(f"[yellow]{item_details_found_prompt}[/yellow]")
    print()
    quantity = get_quantity()
    date_time = datetime.now()
    df = add_item(df, date_time, description, quantity, upc, price, user_identity, current_bin)                            
    auto_save(df)
    print()
    print(df.tail())
    return None