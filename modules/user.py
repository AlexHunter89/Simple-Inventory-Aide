import pyinputplus as pyip
from rich import print
from rich.markup import escape

def greet_and_identify_user():
    #print()
    print("\nWelcome to the inventory tracking system.\n")
    #print()
    user_name_prompt = "Please enter your name: "
    user_name = pyip.inputStr(prompt=user_name_prompt)
    employee_number_prompt = "Please enter your employee number:"
    employee_number = pyip.inputNum(prompt=employee_number_prompt)
    employee_identity = user_name + ": " + str(employee_number)
    print()
    print(f"Welcome: {escape(user_name)}")
    return employee_identity

def warn_user_new_session():
    new_session_overwrite_warning = "[bold red]WARNING![/bold red] Starting a new session will overwrite any previous sessions."
    user_continuation_prompt = "Are you sure you want to continue? (yes/no): "
    print()
    print(new_session_overwrite_warning)
    print()
    user_continuation_response = pyip.inputYesNo(prompt=user_continuation_prompt)
    print()
    return user_continuation_response

def user_change_bin():
    print()
    change_bin_prompt = "Would you like to change the current bin you are working on? (yes/no): "
    change_bin_response = pyip.inputYesNo(prompt=change_bin_prompt)
    return change_bin_response

def get_admin_password():
    password = "admin"
    password_prompt = "Please enter the password: "
    user_password_response = pyip.inputPassword(prompt=password_prompt)
    if user_password_response == password:
        return True
    else:
        return False
    
def feature_coming_soon():
    print()
    print("[blue]Feature coming soon![/blue]")
    print()