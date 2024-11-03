import os
import pandas as pd
import pyinputplus as pyip
from pathlib import Path
from rich import print
from rich.markup import escape

inventory_data_file_path = Path(r"data\inventory.xlsx")
log_file_path = Path(r"data\entry_log.xlsx")
bin_variable_file_path = Path(r"data\bin_variable.txt")

def start_new_inventory_session():
        """Creates an empty DataFrame with appropriate column names."""
        columns = ['DateTime', 'Description', 'Quantity', 'UPC', 'Price', 'User', 'Bin']
        df = pd.DataFrame(columns=columns)
        df = dataframe_types_corrector(df)
        return df

def dataframe_types_corrector(df):
    df = df.astype({
            'DateTime': 'datetime64[ns]',
            'Description': 'string',
            'Quantity': 'int',
            'UPC': 'string',
            'Price': 'float',
            'User': 'string',
            'Bin': 'string'
        })
    return df

def save_entry_log(df):
    df.to_excel(log_file_path, index=False)
    return None


def load_inventory_session():
    new_dataframe_prompt = "Initializing new DataFrame..."
    if os.path.exists(log_file_path):
        try:
            df = pd.read_excel(log_file_path)
        except Exception as e:
            print()
            print(f"Error loading inventory file: {escape(e)}")
            print()
            print(new_dataframe_prompt)
            df = start_new_inventory_session()
    else:
        print()
        print("Could not locate the file.")
        print()
        print(new_dataframe_prompt)
        df = start_new_inventory_session()
    df = dataframe_types_corrector(df)
    return df

def save_inventory_log(df):
    columns_to_drop = ['DateTime', 'User', 'Bin']
    df = df.drop(columns=columns_to_drop)
    df = df.groupby('UPC').agg({
        'Description': 'first',
        'Quantity': 'sum',
        'Price': 'first'
    }).reset_index()
    df = df[['Description', 'Quantity', 'UPC', 'Price']]
    df.to_excel(inventory_data_file_path, index=False)
    return None

def bin_variable_file_handler():
    """Checks to see if a file bin_variable.txt exist.
    If it does, it will read the file and use what is read as the bin variable.
    If it does not, it will create the file and set the bin variable to default '1'."""
    if os.path.exists(bin_variable_file_path):
        bin_variable_file = open(bin_variable_file_path)
        bin_variable = bin_variable_file.read()
        bin_variable_file.close()
        return bin_variable
    else:
        bin_variable = '1'
        bin_variable_file = open(bin_variable_file_path, 'w')
        bin_variable_file.write(bin_variable)
        bin_variable_file.close()
        return bin_variable
    
def bin_changer():
    print()
    enter_bin_number_prompt = "Please enter the bin you would like to work on: "
    new_bin_number = pyip.inputStr(prompt=enter_bin_number_prompt)
    bin_variable_file = open(bin_variable_file_path, 'w')
    bin_variable_file.write(new_bin_number)
    bin_variable_file.close()
    print()
    print(f"Current bin is now set to: {new_bin_number}")
    print()
    return None

def bin_reset():
    bin_variable = '1'
    bin_variable_file = open(bin_variable_file_path, 'w')
    bin_variable_file.write(bin_variable)
    bin_variable_file.close()
    return None

def auto_save(df):
    if (len(df) % 5) == 0:
        save_entry_log(df)
        save_inventory_log(df)
        auto_save_prompt = "[bold green]*(Autosave Complete)*[/bold green]"
        print()
        print(auto_save_prompt)
        print()
        return None
    else:
        return None