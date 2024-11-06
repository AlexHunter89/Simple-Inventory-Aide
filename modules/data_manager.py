import os
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("Error: The module 'pandas' is not installed.")
    print("Please install it by running: python -m pip install pandas")
    exit(1)

try:
    import pyinputplus as pyip
except ImportError:
    print("Error: The module 'pyinputplus' is not installed.")
    print("Please install it by running: python -m pip install pyinputplus")
    exit(1)

try:
    from rich import print
    from rich.markup import escape
except ImportError:
    print("Error: The module 'rich' is not installed.")
    print("Please install it by running: python -m pip install rich")
    exit(1)

inventory_data_file_path = Path(r"data\inventory.xlsx")
log_file_path = Path(r"data\entry_log.xlsx")
bin_variable_file_path = Path(r"data\bin_variable.txt")
password_file_path = Path(r"data\admin.txt")
key_file_path = Path(r"C:\Users\alexj\Documents\open_ai\key_1.txt")

autosave_interval = 5

def open_ai_key_reader():
    """
    Checks for the existence of 'key_1.txt' and reads its value.

    If 'key_1.txt' exists, reads the content and uses it as the Open AI API Key.
    If the file does not exist or contains invalid content,
    it prints a message to the user and returns None.

    Parameters:
        None
    
    Returns:
        str: The Open AI API Key, which was stored in a text file.
        True: If the file is not found or an error occurs while reading the file.

    Notes:
        The Open AI API Key text file is not provided in the GitHub repository.
        You will need to get your own API key and manage the key access in your own unique way.
    """
    try:
        with open(key_file_path, 'r') as file:
            return  file.read().strip()
    except FileNotFoundError:
        print(f"[red]Error: {key_file_path}' not found.[/red]")
        return None

def bin_variable_file_handler():
    """
    Checks for the existence of 'bin_variable.txt' and reads its value.

    If 'bin_variable.txt' exists, reads the content and uses it as the bin variable.
    If the file does not exist or contains invalid content, it creates the file with a default value of '1'.

    Returns:
        str: The bin variable value, which defaults to '1' if no valid data is present.
    """
    if os.path.exists(bin_variable_file_path):
        with open(bin_variable_file_path, 'r') as bin_variable_file:
            bin_variable = bin_variable_file.read().strip()
        return bin_variable
    else:
        bin_variable = '1'
        with open(bin_variable_file_path, 'w') as bin_variable_file:
            bin_variable_file.write(bin_variable)
        return bin_variable

def read_password_from_file():
    """
    Reads the administrator password from an external text file.

    This function attempts to read the administrator password from a file specified by `password_file_path`. 
    The password is returned as a string after stripping any leading or trailing whitespace. If the file 
    cannot be found, an error message is printed, and None is returned.

    Parameters:
        None

    Returns:
        str: The password read from the file, with any extra whitespace removed.
        None: If the file is not found or an error occurs while reading the file.

    Notes:
        - Ensure the password file (`password_file_path`) exists and is accessible.
        - The file should contain the password in plain text, with no extra spaces or lines.
        - For demonstration purposes, this approach is used to externalize the password; however, in production,
          more secure storage methods should be considered.
    """
    try:
        with open(password_file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"[red]Error: Password file '{password_file_path}' not found.[/red]")
        return None

def start_new_inventory_session():
        """
        Creates an empty DataFrame with appropriate column names for inventory tracking.

        The DataFrame is initialized with columns: 'DateTime', 'Description', 'Quantity', 
        'UPC', 'Price', 'User', 'Bin'. The DataFrame is then passed through a type correction 
        function (`dataframe_types_corrector`) to ensure that each column has the correct type.

        Returns:
            pd.DataFrame: A new, empty DataFrame with appropriate column names and corrected types.
        """
        columns = ['DateTime', 'Description', 'Quantity', 'UPC', 'Price', 'User', 'Bin']
        df = pd.DataFrame(columns=columns)
        df = dataframe_types_corrector(df)
        return df

def dataframe_types_corrector(df):
    """
    Converts the columns of the given DataFrame to their appropriate types.

    This function ensures that the DataFrame columns are of the expected data types to maintain
    consistency throughout the inventory tracking process. This is particularly useful when 
    creating new DataFrames or loading data from external sources that may have inconsistent types.

    The following conversions are performed:
        - 'DateTime' is converted to datetime64[ns].
        - 'Description', 'UPC', 'User', and 'Bin' are converted to string.
        - 'Quantity' is converted to pd.Int64Dtype() to allow for missing values (NaN).
        - 'Price' is converted to float.

    Parameters:
        df (pd.DataFrame): The DataFrame to be corrected.

    Returns:
        pd.DataFrame: A DataFrame with columns coerced to the specified types.

    Notes:
        - Columns must exist in the DataFrame before type conversion. This function assumes that 
          the DataFrame has the correct columns present.
        - Using `pd.Int64Dtype()` allows the 'Quantity' column to handle NaN values, which can be 
          useful for incomplete entries.
    """
    df = df.astype({
            'DateTime': 'datetime64[ns]',
            'Description': 'string',
            'Quantity': pd.Int64Dtype(), # Allows NaN values in Quantity
            'UPC': 'string',
            'Price': 'float',
            'User': 'string',
            'Bin': 'string'
        })
    return df

def bin_reset():
    """
    Resets the bin_variable.txt file to '1', creating the file if it does not already exist.

    This function writes the value '1' to the file specified by `bin_variable_file_path`, effectively 
    resetting the bin variable to its default state. If the file does not exist, it will be created 
    automatically. After writing, the function returns the value '1'.

    Parameters:
        None

    Returns:
        str: The bin variable value ('1').

    Notes:
        - This function overwrites any existing value in `bin_variable.txt` with '1'.
        - The file is safely opened in write mode using a context manager to handle automatic closure.
    """
    bin_variable = '1'
    try:
        with open(bin_variable_file_path, 'w') as bin_variable_file:
            bin_variable_file.write(bin_variable)
    except IOError as e:
        print(f"[red]Error: Unable to write to file '{bin_variable_file_path}'. Details: {e}[/red]")
        return None # Return None to indicate an error occurred
    return bin_variable

def load_inventory_session():
    """
    Loads the inventory session from an existing log file or creates a new session.

    This function attempts to load an inventory session from an Excel log file. If the file cannot be 
    found or there is an error loading it, a new inventory DataFrame is created. The resulting DataFrame 
    is then passed through `dataframe_types_corrector` to ensure all columns are of the correct types.

    Parameters:
        None

    Returns:
        pd.DataFrame: A DataFrame containing the inventory data, either loaded from a previous session or newly created.
    
    Notes:
        - The inventory log file is expected to be in Excel format (`.xlsx`). Ensure `log_file_path` points to a valid file.
        - If the file cannot be found or loaded, a new session will be initialized.
    """
    previous_dataframe_prompt = "\n[green]*Previous Session Loaded*[/green]\n"
    new_dataframe_prompt = "Initializing new DataFrame...\n"

    if os.path.exists(log_file_path):
        try:
            df = pd.read_excel(log_file_path)
            print(previous_dataframe_prompt)
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

def bin_changer():
    """
    Allows the user to change the current bin by entering a new bin identifier.

    Prompts the user to enter a new bin number and writes this value to the `bin_variable.txt` file.
    After updating the file, it prints a confirmation message displaying the new bin value and returns the new bin value.

    Parameters:
        None

    Returns:
        str: The new bin value set by the user.

    Notes:
        - The function writes the new bin value to the `bin_variable.txt` file, replacing any existing value.
        - If an error occurs while writing to the file, an appropriate error message will be displayed.
    """
    enter_bin_number_prompt = "\nPlease enter the bin you would like to work on: "
    new_bin_number = pyip.inputStr(prompt=enter_bin_number_prompt)
    
    try:
        with open(bin_variable_file_path, 'w') as bin_variable_file:
            bin_variable_file.write(new_bin_number)
        print(f"\n[green]Current bin is now set to: {escape(new_bin_number)}[/green]\n")
        return new_bin_number
    except IOError as e:
        print(f"[red]Error: Unable to write to file '{bin_variable_file_path}'. Details: {e}[/red]")
        return None

def save_inventory_log(df):
    """
    Saves a summary of the inventory log.
    
    Args:
        df (DataFrame): The inventory DataFrame.
    
    Returns:
        None
    """
    columns_to_drop = ['DateTime', 'User', 'Bin']   # Drop unneeded columns and aggregate data for inventory summary
    df = df.drop(columns=columns_to_drop)

    df = df.groupby('UPC').agg({
        'Description': 'first',
        'Quantity': 'sum',
        'Price': 'first'
    }).reset_index()

    df = df[['Description', 'Quantity', 'UPC', 'Price']]
    df.to_excel(inventory_data_file_path, index=False)
    return None

def save_entry_log(df):
    """
    Saves a detailed entry log of all inventory data.
    
    Args:
        df (DataFrame): The inventory DataFrame.
    
    Returns:
        None
    """
    df.to_excel(log_file_path, index=False)
    return None
    
def auto_save(df):
    """
    Automatically saves the inventory data if the number of entries reaches a specified interval.
    
    Args:
        df (DataFrame): The inventory DataFrame.
        autosave_interval (int): The interval at which autosave is triggered.
    
    Returns:
        None
    """
    if (len(df) % autosave_interval) == 0:
        save_entry_log(df)
        save_inventory_log(df)
        auto_save_prompt = "\n[bold green]*(Autosave Complete)*[/bold green]\n"
        print(auto_save_prompt)
        return None
    else:
        return None