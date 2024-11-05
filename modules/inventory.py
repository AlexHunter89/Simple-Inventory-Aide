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
    """
    Adds a new item to the inventory DataFrame.
    
    Args:
        df (DataFrame): The current inventory DataFrame.
        date_time (datetime): The current timestamp.
        description (str): The description of the new item.
        quantity (int): The quantity of the new item.
        upc (str): The UPC code of the new item.
        price (float): The price of the new item.
        user_identity (str): The identity of the user adding the item.
        current_bin (str): The identifier for the current inventory bin.
    
    Returns:
        DataFrame: The updated inventory DataFrame.
    
    Raises:
        ValueError: If any of the required values are invalid.
    """
    if not validate_item_inputs(description, quantity, price, upc): # Step 1: Validate inputs
        raise ValueError("Invalid input values for new item.")
    
    new_item = construct_item(date_time, description, quantity, upc, price, user_identity, current_bin) # Step 2: Construct the new item

    df.loc[len(df)] = new_item  # Step 3: Add the item to the DataFrame

    return df

def construct_item(date_time, description, quantity, upc, price, user_identity, current_bin):
    """
    Constructs a dictionary for the new item being added to the inventory.
    
    Args:
        date_time (datetime): The current timestamp.
        description (str): The description of the new item.
        quantity (int): The quantity of the new item.
        upc (str): The UPC code of the new item.
        price (float): The price of the new item.
        user_identity (str): The identity of the user adding the item.
        current_bin (str): The identifier for the current inventory bin.
    
    Returns:
        dict: A dictionary representing the new item.
    """
    return {
        'DateTime': date_time,
        'Description': description,
        'Quantity': quantity,
        'UPC': upc,
        'Price': price,
        'User': user_identity,
        'Bin': current_bin
    }

def validate_item_inputs(description, quantity, price, upc):
    """
    Validates the inputs for the item being added to the inventory.
    
    Args:
        description (str): The item description.
        quantity (int): The quantity of the item.
        price (float): The price of the item.
        upc (str): The UPC code of the item.
    
    Returns:
        bool: True if all inputs are valid, False otherwise.
    """
    if not isinstance(description, str) or description.strip() == "":
        return False
    if not isinstance(quantity, int) or quantity < 0:
        return False
    if not isinstance(price, (int, float)) or price <= 0:
        return False
    if not isinstance(upc, str) or len(upc) != 12:
        return False
    return True

def item_not_found_sequence(df,  upc, user_identity, current_bin):
    """
    Handles the scenario where an item with the given UPC code is not found in the inventory.
    
    This function guides the user through adding a new item to the inventory when an unknown UPC is entered.
    It includes several steps such as notifying the user, gathering item details (description, price, and quantity),
    adding the item to the inventory DataFrame, and saving the updated inventory data. The function ensures data integrity
    by allowing the user to cancel the operation at any stage.
    
    Args:
        df (DataFrame): The current inventory DataFrame.
        upc (str): The UPC code of the item that was not found in the inventory.
        user_identity (str): The identity of the user performing the operation.
        current_bin (str): The identifier for the current inventory bin where the item is being added.
    
    Steps:
        1. Notify the user that the item was not found in the inventory.
        2. Gather new item details such as description and price.
            - If the user chooses to cancel the process, the function stops and returns to the main menu.
        3. Gather quantity details for the new item.
            - If the user enters a quantity of 0, the function stops and returns to the main menu.
        4. Record the current timestamp for the entry.
        5. Add the new item to the inventory DataFrame with all gathered details.
        6. Automatically save the inventory data every 5 entries.
        7. Display the last few rows of the updated inventory to confirm the addition.

    Returns:
        None: The function updates the DataFrame in-place and handles all subsequent actions without returning a value.
    
    Notes:
        - The function ensures that the user can cancel at any point if they decide not to add the item.
        - Autosave is triggered every 5 entries to minimize data loss risks.
        - Data persistence is handled through calls to `auto_save()`, which saves a full entry log and an inventory summary.
    """
    # Step 1: Notify the user that the item wasn't found
    item_details_needed_prompt = "\n[yellow]Could not find item in database. Please enter the details.[/yellow]\n"
    print(item_details_needed_prompt)

    description, price = get_item_details() # Step 2: Gather the new item details

    if description is None and price is None:
        print("No item added. Returning to main menu.")
        return None # If user cancels entry, stop further processing.

    quantity = get_quantity()   # Step 3: Gather quantity details

    if quantity == 0:   # Step 4: Handle zero quantity
        print("No quantity added. Returning to main menu.")
        return None # Stop further processing if quantity is zero.

    date_time = datetime.now()  # Step 5: Get the current timestamp

    # Step 6: Add the new item to the inventory DataFrame
    df = add_item(df, date_time, description, quantity, upc, price, user_identity, current_bin)

    auto_save(df)   # Saves data every 5 entries

    print() # Print some space and then the previous 5 entries
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