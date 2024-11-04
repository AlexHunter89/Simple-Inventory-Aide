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

def greet_and_identify_user():
    """Greets the user. Asks them for their name and employee number. Does not validate user information. Employee number must be in integer. Returns an 'identity'."""
    print("\nWelcome to the inventory tracking system.\n")
    user_name_prompt = "Please enter your name: "
    user_name = pyip.inputStr(prompt=user_name_prompt, strip=True)
    employee_number_prompt = "Please enter your employee number: "
    employee_number = pyip.inputNum(prompt=employee_number_prompt, strip=True)
    employee_identity = user_name + ": " + str(employee_number)
    print(f"\nWelcome: {escape(user_name)}")
    return employee_identity