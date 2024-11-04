import pyinputplus as pyip
from rich import print
from rich.markup import escape

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

def new_session_warning_sequence():
    """Warns the user about the data overwrite that will occur when starting a new session.
    Ask them to confirm their action. This action should be reserved to administrators."""
    new_session_overwrite_warning = "\n[bold red]WARNING![/bold red] Starting a new session will overwrite any previous sessions.\n"
    user_continuation_prompt = "Are you sure you want to continue? (yes/no): "
    print(new_session_overwrite_warning)
    user_continuation_response = pyip.inputYesNo(prompt=user_continuation_prompt)
    print()
    if user_continuation_response == 'yes':
        password = 'admin'
        password_prompt = "Please enter the password: "
        user_password_response = pyip.inputPassword(prompt=password_prompt)
        if user_password_response == password:
            print("\n[green]*New Session Started*[/green]\n")
            return True
        else:
            print("\n[bold red]Access Denied[/bold red]\n")
            return False
    else:
        return False


def user_change_bin():
    change_bin_prompt = "\nWould you like to change the current bin you are working on? (yes/no): "
    change_bin_response = pyip.inputYesNo(prompt=change_bin_prompt)
    return change_bin_response

    
def feature_coming_soon():
    print("\n[blue]Feature coming soon![/blue]\n")