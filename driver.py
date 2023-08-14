from models.user_credentials import UserCredential
from database import Database
from datetime import datetime

from models.user_entities import User


def print_welcome_prompt():
    print("Welcome to this Quiz Program Portal.")
    print("Today's date & time is: " + datetime.now().strftime("%d/%m/%Y") + " & " + datetime.now().strftime("%H:%M:%S"))


def authenticate() -> User:
    current_user = None
    while True:
        print("Available roles: \"student\", \"admin\", or \"quit\" to quit")
        role = input("* Enter role: ")
        if role.lower() == "admin":
            while True:
                print("Available options: register, login")
                option = input("* Enter option: ")
                if option.lower() == "register":
                    print("To get started, enter the secret obtained from your network administrator:-")
                    attempts = 3
                    secret_authenticated = False
                    while True:
                        secret = input("* Enter secret: ")
                        if secret != "secret":
                            attempts -= 1
                            print("Wrong secret entered. You have " + str(attempts) + "/3 attempts left.")
                            if attempts == 0:
                                break
                            continue
                        else:
                            secret_authenticated = True
                            break
                    if not secret_authenticated:
                        continue
                    print("Create a new username & password:-")
                    while True:
                        user_name = input("* Enter username: ")
                        if len(user_name) > 0:
                            break
                    while True:
                        user_password = input("* Enter password: ")
                        if len(user_password) > 0:
                            break
                    current_user = Database.add_user(user_name, user_password, UserCredential.ROLES["admin"])
                    print("Registered successfully. Make sure you remember your credentials in order to login later.")
                    return current_user
                elif option.lower() == "login":
                    attempts = 3
                    user_authenticated = False
                    while True:
                        user_name = input("* Enter username: ")
                        if len(user_name) > 0:
                            break
                    while True:
                        user_password = input("* Enter password: ")
                        if len(user_password) < 0:
                            continue
                        else:
                            current_user = Database.fetch_user(user_name, user_password)
                            if current_user is None:
                                attempts -= 1
                                print("Wrong credentials entered. You have " + str(attempts) + "/3 attempts left.")
                                if attempts == 0:
                                    break
                                continue
                            else:
                                user_authenticated = True
                    if user_authenticated:
                        print("Logged in successfully...")
                        return current_user
                else:
                    print("Invalid option (" + role + "). Tip: Type \"quit\" to exit.")
        elif role.lower() == "student":
            while True:
                print("Available options: register, login")
                option = input("* Enter option: ")
                if option.lower() == "register":
                    print("Create a new username & password:-")
                    while True:
                        user_name = input("* Enter username: ")
                        if len(user_name) > 0:
                            break
                    while True:
                        user_password = input("* Enter password: ")
                        if len(user_password) > 0:
                            break
                    current_user = Database.add_user(user_name, user_password, UserCredential.ROLES["student"])
                    print("Registered successfully. Make sure you remember your credentials in order to login later.")
                    return current_user
                elif option.lower() == "login":
                    attempts = 3
                    user_authenticated = False
                    while True:
                        user_name = input("* Enter username: ")
                        if len(user_name) > 0:
                            break
                    while True:
                        user_password = input("* Enter password: ")
                        if len(user_password) < 0:
                            continue
                        else:
                            current_user = Database.fetch_user(user_name, user_password)
                            if current_user is None:
                                attempts -= 1
                                print("Wrong credentials entered. You have " + str(attempts) + "/3 attempts left.")
                                if attempts == 0:
                                    break
                                continue
                            else:
                                user_authenticated = True
                    if user_authenticated:
                        print("Logged in successfully...")
                        return current_user
                else:
                    print("Invalid option (" + role + "). Tip: Type \"quit\" to exit.")
        elif role.lower() == "quit":
            print("Quitting...")
            exit(0)
        else:
            print("Invalid role (" + role + "). Tip: Type \"quit\" to exit.")


def enter_admin_mode(current_user):
    print("admin mode")
    pass


def enter_student_mode(current_user):
    print("user mode")
    pass


def main():
    print_welcome_prompt()
    current_user = authenticate()
    if current_user.get_credentials().get_role() == UserCredential.ROLES["admin"]:
        enter_admin_mode(current_user)
    elif current_user.get_credentials().get_role() == UserCredential.ROLES["student"]:
        enter_student_mode(current_user)


if __name__ == "__main__":
    main()
