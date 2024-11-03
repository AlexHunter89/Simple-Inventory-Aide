import pyinputplus as pyip
from datetime import datetime
from modules.data_manager import auto_save
from rich import print

def get_upc():
    while True:
        """Prompt the user to enter a UPC code."""
        upc_entry_prompt = "Please enter a UPC code (Or press Enter to save and return to the Main Menu): "
        print()
        upc = pyip.inputNum(prompt=upc_entry_prompt, blank=True)
        if upc == '':
            break
        elif len(str(upc)) == 12:
            break
        else:
            print("Invalid UPC length.")
            continue
    return upc

def get_item_details():
    """Prompt the user for item description and price."""
    description_entry_prompt = "Please enter the item description: "
    price_entry_prompt = "Please enter the item price: "
    description = pyip.inputStr(prompt=description_entry_prompt)
    price = pyip.inputNum(prompt=price_entry_prompt)
    return (description, price)

def get_existing_upc_data(upc, df):
    matches = df[df['UPC'] == upc]
    if not matches.empty:
        previous_entry = matches.iloc[0]
        description = previous_entry['Description']
        price = previous_entry['Price']
        return (description, price)
    else:
        return (None, None)
    
def get_quantity():
    """Prompt the user for quantity of items."""
    quantity_entry_prompt = "Please enter the quantity (Can enter 0 if you don't want to update the quantity): "
    quantity = pyip.inputNum(prompt=quantity_entry_prompt, min=0)
    return quantity

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
    item_details_needed_prompt = "Could not find item in database. Please enter the details."
    print()
    print(f"[yellow]{item_details_needed_prompt}[/yellow]")
    print()
    description, price = get_item_details()
    quantity = get_quantity()
    date_time = datetime.now()
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