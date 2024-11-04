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
    print("\n[green]*Previous Session Loaded*[/green]")
    new_dataframe_prompt = "Initializing new DataFrame..."
    if os.path.exists(log_file_path):
        try:
            df = pd.read_excel(log_file_path)
        except Exception as e:
            print(f"\nError loading inventory file: {escape(e)}\n")
            print(new_dataframe_prompt)
            df = start_new_inventory_session()
    else:
        print("\nCould not locate the file.\n")
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
    enter_bin_number_prompt = "\nPlease enter the bin you would like to work on: "
    new_bin_number = pyip.inputStr(prompt=enter_bin_number_prompt)
    bin_variable_file = open(bin_variable_file_path, 'w')
    bin_variable_file.write(new_bin_number)
    bin_variable_file.close()
    print(f"\nCurrent bin is now set to: {escape(new_bin_number)}\n")
    return None

def bin_reset():
    """Resets the bin_variable.txt file to '1'. Creates the file automatically if it doesn't already exist. Returns the bin variable."""
    bin_variable = '1'
    bin_variable_file = open(bin_variable_file_path, 'w')
    bin_variable_file.write(bin_variable)
    bin_variable_file.close()
    return bin_variable

def auto_save(df):
    if (len(df) % 5) == 0:
        save_entry_log(df)
        save_inventory_log(df)
        auto_save_prompt = "\n[bold green]*(Autosave Complete)*[/bold green]\n"
        print(auto_save_prompt)
        return None
    else:
        return None