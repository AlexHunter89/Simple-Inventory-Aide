# Inventory Tracking System

## Update: Major Refactoring in Progress

Hello, everyone! I wanted to share a quick update regarding some ongoing improvements to the project.

I am currently conducting a significant refactoring of the code base to improve readability and maintainability. As part of this process, I’m also adding docstrings across the code to facilitate easier collaboration and understanding for anyone interested in contributing.

However, please be aware that during this overhaul, the DataFrame functionality is temporarily impacted, particularly with recognizing preexisting UPCs in the database. I’m actively working to resolve these issues as part of the overall refactoring and bug-squashing effort. I expect to have everything back in working order within the next day or two.

Thank you for your patience, and stay tuned for updates!

## Overview

This Inventory Tracking System is a command-line Python application designed to manage inventory by scanning or manually entering UPC (Universal Product Code) numbers. The program helps users track item descriptions, prices, and quantities. If an item is already present in the inventory, the user can simply update the quantity. If the item is new, the system will prompt the user to provide additional details, such as a description and price. This software is perfect for small-scale inventory management where simple text-based tracking is sufficient.

The program also includes various menu options that allow users to start a new session, load previous inventory data, modify entries, or switch between different storage bins.

## Features
- **User Authentication:** Users are identified by their name and employee number.
- **Inventory Management:** The program tracks items by UPC, allowing the user to add new items or update existing items.
- **Data Persistence:** Inventory data is saved automatically and periodically to avoid data loss.
- **Bin Management:** Users can organize inventory into different storage bins and switch bins as needed.
- **Autosave Functionality:** The program automatically saves data after every five entries, ensuring up-to-date records.

## Installation

Before you start using the program, make sure you have Python installed. You will also need to install the required dependencies listed in the `requirements.txt` file.

To install dependencies, run:

```sh
pip install -r requirements.txt
```

The required libraries include:
- **pandas** for data handling.
- **rich** for enhanced console output.
- **pyinputplus** for user prompts.

For more details, refer to the `requirements.txt` file.

## How to Run

To start the program, simply run the `main.py` file:

```sh
python main.py
```

Upon launching, the program will greet you and ask for your name and employee number. You will then be presented with a menu of options for managing the inventory.

## User Guide

1. **Welcome and User Identification**
   - The program starts by greeting the user and asking for their name and employee number to establish user identity.

2. **Menu Options**
   - **Start New Session (Not Recommended):** This option allows users to start a new inventory session from scratch. Please note that any existing data will be overwritten if a new session is started.
   - **Load Previous Session (Recommended):** Loads the last saved inventory session, allowing you to continue managing items.
   - **Delete Entry / Modify Entry:** Currently, these options are placeholders and will be implemented in future versions.
   - **Change Current Bin:** Allows users to change the current bin they are working on, enabling easy categorization of inventory.
   - **Exit:** Closes the program.

3. **Adding Items to Inventory**
   - After selecting either **Start New Session** or **Load Previous Session**, the user can enter UPC numbers.
   - If the UPC exists, the program retrieves the item's previous description and price, and only asks for a quantity update.
   - If the UPC is new, the user is prompted to enter the item's description and price, followed by quantity.

4. **Managing Bins**
   - Users can switch bins to track inventory separately in different locations or categories. When changing bins, the program updates the current bin being worked on.

5. **Autosave Feature**
   - The inventory data is automatically saved after every five entries to prevent data loss. The data is saved in two formats: session logs and inventory logs.

## Data Files
- **Inventory Data** is saved in an Excel file (`data/inventory.xlsx`), making it easy to load the previous inventory and continue where you left off.
- **Session Logs** are also maintained to help with record-keeping.
- **Bin Information** is saved in a text file (`data/bin_variable.txt`) to track which bin is currently in use.

## Example Usage

Here is a basic flow of how a user might interact with the system:

1. Start the program by running `main.py`.
2. Enter your name and employee number.
3. Choose "Load Previous Session" to continue adding items.
4. Enter a UPC code.
   - If the item exists, enter the quantity to update.
   - If the item is new, enter the description, price, and quantity.
5. If you need to switch to another bin, select "Change Current Bin" from the main menu.
6. When done, select "Exit" to quit the program.

## Requirements
The full list of required libraries is in the `requirements.txt` file, but the key dependencies are:
- `pandas` for managing inventory data.
- `rich` for pretty console output.
- `pyinputplus` for robust user input handling.

## Future Features
- **Delete Entry** and **Modify Entry** functionalities are placeholders and will be added in future versions.
- Improved item tracking and bin categorization will be implemented based on user feedback.

## Contributing
Contributions are welcome! If you would like to contribute to this project, please fork the repository and create a pull request. Bug reports and feature requests can be submitted via the Issues section.

## License
This project is licensed under the MIT License.

---

Feel free to reach out with any questions or suggestions to help improve the Inventory Tracking System. Your feedback is greatly appreciated!

