from app.database.database_manager import DatabaseManager, SuperDatabaseManager
from app.services.user_manager import UserManager
from app.services.table_manager import TableManager
from app.models.user import UserRoles
from dotenv import load_dotenv
import os
from app.utils.validators import get_input, get_valid_choice
load_dotenv()

class DefaultAdmin:
    def __init__(self, username):
        self.username = username
        self.roles = UserRoles("admin")

def login(db_manager, us_manager):
     
     
    while True:
        username = get_input(str, "Please enter your username: ")
        password = get_input(str, "Please enter your password: ")
        def_user = os.getenv("DEFAULT_ADMIN_USERNAME")
        def_pass = os.getenv("DEFAULT_ADMIN_PASSWORD")
        if username ==  def_user and password == def_pass:
            print("Logged in as default admin.")
            input("\nPress Enter to continue...")
            return True, DefaultAdmin(username)
        try:
            result, user_object, text = us_manager.login(username, password)
            if result:
                print(text)
                input("\nPress Enter to continue...")
                return True, user_object
            else:
                print(text)
                choice = input("Will you try again?[Y/N]").strip().upper()
                if choice in ["N","NO", "NAKHER","NA"]:
                    return False, None
        except Exception as er:
            print(f"Error: {er}")
            input("\nPress Enter to continue...")
            return False, None

def user_registration(us_manager: UserManager):
    username = get_input(str, "Please enter a new username: ")
    password = get_input(str, "Please enter a new password: ")
    role = get_valid_choice(['admin', 'waiter'], "Please select a role (admin, waiter): ")
    role_obj = UserRoles(role)
    result, info = us_manager.register(username, password, role_obj)
    if not result:
        print(info)
        input("\nPress Enter to return...")
        return
    print(f"Username: {info.username} | ID {info.id}  was successfully added.")
    input("\nPress Enter to return...")

def delete_username(us_manager: UserManager):
    username = get_input(str, "Please enter a username: ")
    result, info = us_manager.delete_user(username)
    print(info)
    input("\nPress Enter to return...")

def change_password_password(us_manager: UserManager):
    username = get_input(str, "Please enter a username: ")
    old_password = get_input(str, "Please enter a old password: ")
    new_password = get_input(str, "Please enter a new password: ")
    result, info = us_manager.change_password(username, old_password, new_password)
    print(info)
    input("\nPress Enter to return...")

def show_assign_tables_all_waiter(us_manager: UserManager):
    result, data = us_manager.get_assign_tables_all_waiter()
    if not result:
        print(data)
        input("\nPress Enter to return...")
    for item in data:
        print(f"ID: {item.id}, Username: {item.username}, Roles: {item.roles.value}")
        for assigned_table in item.assigned_tables:
            print("|________", f"ID: {assigned_table.id}, Table Number: {assigned_table.table_number}, Status: {assigned_table.status.value}")
    input("\nPress Enter to return...")

def add_assign_table_to_waiter(us_manager: UserManager, ta_manager: TableManager):
    username = get_input(str, "Please enter a username: ")
    table_number = get_input(int, "Please enter the table number: ")
    result, obj = ta_manager.existence_table(table_number)
    if not result:
        print("The requested table was not found.")
        input("\nPress Enter to return...")
    res, info = us_manager.assign_table_to_waiter(username, obj.id)
    print(info)
    input("\nPress Enter to return...")

def remove_assign_tables_all_waiter(us_manager: UserManager, ta_manager: TableManager):
    username = get_input(str, "Please enter a username: ")
    table_number = get_input(int, "Please enter the table number: ")
    result, obj = ta_manager.existence_table(table_number)
    if not result:
        print("The requested table was not found.")
        input("\nPress Enter to return...")
    res, info = us_manager.remove_table_from_waiter(username, obj.id)
    print(info)
    input("\nPress Enter to return...")
    

def restaurant_menu(user_obj, us_manager: UserManager, ta_manager: TableManager):
    actions = {
    "1": ("Add a new username", lambda: user_registration(us_manager)),
    "2": ("Delete a username", lambda: delete_username(us_manager)),
    "3": ("Change username's password", lambda: change_password_password(us_manager)),
    "4": ("View tables assigned to all waiters", lambda: show_assign_tables_all_waiter(us_manager)),
    "5": ("Add Assign table to waiter", lambda: add_assign_table_to_waiter(us_manager, ta_manager)),
    "6": ("Remove Assign table to waiter", lambda: remove_assign_tables_all_waiter(us_manager, ta_manager)),
    }
    while True:
        print("+-"*20)
        for key, (title, _) in actions.items():
            print(f"{key}. {title}")
        print("+-"*20)
        choice = input("Select: ")

        if choice == "0":
            break

        action_data = actions.get(choice)

        if action_data:
            _,action_fun = action_data
            action_fun()
        else:
            print("Invalid option")
    ...
def waiter_menu():
    ...
def database_menu(db_manager: DatabaseManager):
    sdb_manager = SuperDatabaseManager()
    re, info = sdb_manager.create_database()
    print("-"*20)
    print(info)
    print("-"*20)
    if not re:
        input("\nPress Enter to return...")
        return False
    input("\nPress Enter to continue...")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(BASE_DIR, "database", "schema.sql")
    res = db_manager.run_script_file(schema_path)
    if not res:
        print("Tables could not be created")
        input("\nPress Enter to return...")
        return False
    trigger_path = os.path.join(BASE_DIR, "database", "triggers.sql")
    print("="*20)
    print("Tables were created")
    print("="*20)
    input("\nPress Enter to continue...")
    resu = db_manager.run_script_file(trigger_path)
    if not resu:
        print("Triggers were not created.")
        input("\nPress Enter to return...")
        return False
    print("*"*20)
    print("Triggers were successfully created.")    
    print("*"*20)
    input("\nPress Enter to return...")


def main_menu():
    db_manager = DatabaseManager()
    us_manager = UserManager(db_manager)
    ta_manager = TableManager(db_manager)
    logged_in, user_obj = login(db_manager, us_manager)
    if not logged_in:
        return
    
    while True:
        result, info = db_manager.get_connect()
        
        print(20*"=|")
        print("1. Restaurant Management")
        print("2. Waiter Orders")
        print("3. Database Management")
        print("0. Exit")
        print(20*"=|")
        print()

        choice = input("Select: ")

        match choice:
            case "1":
                if not result:
                    print("First, create the database in option 3.")
                    input("\nPress Enter to continue...")
                    continue
                if user_obj.roles.value == "admin":
                    restaurant_menu(user_obj, us_manager, ta_manager)
                else:
                    print("You do not have access to this section.")
                    input("\nPress Enter to continue...")

            case "2":
                if not result:
                    print("First, create the database in option 3.")
                    input("\nPress Enter to continue...")
                    continue
                waiter_menu(user_obj)

            case "3":
                if user_obj.roles.value == "admin" and not result:
                    database_menu(db_manager)

            case "0":
                break

            case _:
                print("Invalid option")

if __name__ == "__main__":
    main_menu()