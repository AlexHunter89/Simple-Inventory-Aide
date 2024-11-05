# Inventory Tracking System

## Update: Major Refactoring Complete – Code Readability & Bug Fixes

Hello everyone! I’m thrilled to share that I’ve completed a significant refactoring of the codebase to greatly enhance readability, maintainability, and functionality.

Key improvements include:

Enhanced Code Readability: Major sections of the code have been rewritten with clearer logic flows, making it much easier to understand and navigate. Each menu option now follows a distinct, easy-to-track path for better separation of concerns.
Comprehensive Docstrings: Added detailed docstrings throughout the code to facilitate easier onboarding for new contributors and improve long-term maintainability.
Bug Fixes: Fixed an issue that affected the recognition of preexisting UPCs in the database. The workflow for managing inventory entries, especially with distinguishing between new and existing items, has been streamlined. The DataFrame interactions are now more robust, ensuring smoother operations.
This refactor not only fixes existing bugs but also provides a solid foundation for adding new features and tracking data more effectively in the future.

Thank you all for your patience during this refactoring process! The code is back in working order, and I’m looking forward to any feedback or contributions you might have.

## Overview

Welcome to the Inventory Tracking System! This Python-based text interface program helps users track and manage inventory items using Universal Product Codes (UPCs). Users can scan or enter UPCs, manage item details, and organize items into bins for better categorization. Whether you're starting fresh or continuing from a previous inventory session, this system is designed to make inventory management smooth and straightforward.

## Features

- **User Identification**: Each session begins by greeting the user and identifying them by name and employee number. For example, you will be prompted to enter your name and your employee number, and then see a message like 'Welcome: John Doe, Employee #1234'. Each session begins by greeting the user and identifying them by name and employee number.
- **UPC Scanning and Item Management**: Enter UPCs to check if items are already recorded. If an item exists, simply add a quantity. If not, enter item details such as description and price.
- **Multiple Bins**: Organize items into different inventory bins for better categorization.
- **Autosave Functionality**: Inventory data is saved automatically after a set number of entries to prevent data loss. Users do not need to manually save their work, as the autosave feature ensures that all changes are regularly backed up.

## Requirements

To use the Inventory Tracking System, you will need to install the dependencies listed in `requirements.txt`.

Install them by running:

```sh
pip install -r requirements.txt
```

## How to Use

1. **Launch the Program**:
   
   Run the main script to start the program:
   ```sh
   python main.py
   ```

2. **User Identification**:
   
   The system will greet you and ask for your name and employee number. This information is used to identify the user and is displayed during the session.

3. **Main Menu Options**:

   After user identification, you will see the following menu options, each designed to guide you through inventory management:

   - **Start New Session (Not Recommended)**: Begins a new inventory session, which will overwrite any previous session data. You will need to confirm and provide an admin password to proceed.
   - **Load Previous Session (Recommended)**: Loads the last saved inventory session, allowing you to continue where you left off.
   - **Delete Entry (Coming Soon)**: Placeholder for a future feature to delete items from inventory.
   - **Modify Entry (Coming Soon)**: Placeholder for a future feature to modify item details.
   - **Change Current Bin**: Allows you to switch to a different inventory bin for better organization of items.
   - **Exit**: Ends the session and closes the program.

4. **Inventory Management**:
   - **Entering UPCs**: You will be prompted to enter a UPC code. If the code is already in the inventory, you can add a quantity. If it's a new item, you will be asked to provide additional details.
   - **Adding New Items**: If the UPC is not found, you'll be guided to enter the item description, price, and quantity. The data is recorded along with a timestamp and user details.
   - **Changing Bins**: You can change the bin in which the item will be stored, allowing for more organized inventory management.

5. **Autosave**:
   
   The system automatically saves inventory data every 5 entries. This ensures that all changes are consistently backed up without requiring manual intervention.

## Data Persistence

- **Inventory Data**: Inventory information is saved in an Excel file (`data/inventory.xlsx`). A detailed entry log is also saved as `data/entry_log.xlsx`. Please note that users may need to manually check and back up these files if additional data security is required. Inventory information is saved in an Excel file (`data/inventory.xlsx`). A detailed entry log is also saved as `data/entry_log.xlsx`.
- **User Authentication**: Administrator actions (such as starting a new session) require a password, which is read from the file `data/admin.txt`. Please make sure this file exists and is correctly configured.

## Handling Errors

- **Module Imports**: Ensure all necessary modules (`pandas`, `rich`, `pyinputplus`) are installed. If any of these modules are missing, the program will prompt you to install them. If you encounter issues with module installation, try running the following command to install the required module:
  ```sh
  pip install module_name
  ``` Ensure all necessary modules (`pandas`, `rich`, `pyinputplus`) are installed. If any of these modules are missing, the program will prompt you to install them.
- **File Handling**: Make sure required data files (e.g., `inventory.xlsx`, `entry_log.xlsx`, `bin_variable.txt`, `admin.txt`) are available and accessible.

## Dependencies

This project uses the following Python libraries:

- **pandas**: For handling data storage and manipulation.
- **rich**: For improved console output.
- **pyinputplus**: For user input handling with additional validation.

All dependencies are listed in `requirements.txt`. Run the following command to install them:

```sh
pip install -r requirements.txt
```

## Known Issues and Limitations

- The **Delete Entry** and **Modify Entry** features are currently placeholders and will be implemented in future versions.
- For the best experience, users are recommended to load a previous session rather than starting a new one, as starting a new session will overwrite all previous data.

## Contributing

Contributions to enhance this system are welcome! Please fork the repository, make changes, and submit a pull request. Feel free to add new features, enhance existing functionality, or improve the user interface.

## License

This project is open-source and available under the MIT License.

## Contact

For any questions or issues, please open an issue on the repository or contact the maintainer directly.

---
Thank you for using the Inventory Tracking System. We hope it makes managing your inventory easier and more efficient!