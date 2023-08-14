from security.authentication import Authenticator
from models.database import Database
from datetime import datetime


def print_welcome_prompt():
    print("-------------------------------------")
    print("Welcome to this Quiz Program Portal.")
    print("Today's date & time is: " + datetime.now().strftime("%d/%m/%Y") + " & " + datetime.now().strftime("%H:%M:%S"))
    print("--------------------------------------------------------------------------")


def authenticate(database):
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
                    current_user = database.add_user(user_name, user_password, Authenticator.ROLES["admin"])
                    print("Registered successfully.")
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
                        if len(user_password) == 0:
                            continue
                        else:
                            current_user = database.fetch_user(user_name, user_password)
                            if current_user is None:
                                attempts -= 1
                                print("Wrong credentials entered. You have " + str(attempts) + "/3 attempts left.")
                                if attempts == 0:
                                    break
                                continue
                            else:
                                user_authenticated = True
                        if user_authenticated:
                            print("Logged in successfully.")
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
                    current_user = database.add_user(user_name, user_password, Authenticator.ROLES["student"])
                    print("Registered successfully.")
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
                        if len(user_password) == 0:
                            continue
                        else:
                            current_user = database.fetch_user(user_name, user_password)
                            if current_user is None:
                                attempts -= 1
                                print("Wrong credentials entered. You have " + str(attempts) + "/3 attempts left.")
                                if attempts == 0:
                                    break
                                continue
                            else:
                                user_authenticated = True
                    if user_authenticated:
                        print("Logged in successfully.")
                        return current_user
                else:
                    print("Invalid option (" + role + "). Tip: Type \"quit\" to exit.")
        elif role.lower() == "quit":
            print("No changes made. Quitting...")
            exit(0)
        else:
            print("Invalid role (" + role + "). Tip: Type \"quit\" to exit.")


def print_quizzes_list(database):
    quizzes = database.fetch_all_quizzes()
    print("------------------------------------------------------------")
    if len(quizzes) == 0:
        print("No quizzes exist in the database. Add a quiz to get started.")
        print("------------------------------------------------------------")
        return
    print("Viewing all quizzes:-")
    print("---------------------")
    for quiz in quizzes.values():
        print("- Quiz name: " + quiz["name"], ", ID: " + str(quiz["id"]) + ", Creator: " + quiz["owner_name"])
        question_number = 1
        for question in quiz["questions"]:
            print("Question(" + str(question_number) + "): " + question["title"])
            question_number += 1
            choice_number = 1
            for choice in question["choices"]:
                print(str(choice_number) + ") " + choice)
                choice_number += 1
            print()
        print("------------------------------------")


def print_add_quiz_form(database, current_user):
    while True:
        print("--------------------------")
        print("Viewing add a quiz form:-")
        while True:
            quiz_name = input("* Quiz name: ")
            if len(quiz_name) > 0:
                break
        while True:
            quiz_subject = input("* Quiz subject: ")
            if len(quiz_subject) > 0:
                break
        question_number = 1
        quiz_questions = []
        while True:
            print("Type \"add\" to add a question to quiz (" + quiz_name + "), \"save\" to save the quiz, or \"discard\" to discard the form:-")
            option = input("* Option: ")
            if option == "add":
                quiz_question_choices = []
                while True:
                    quiz_question_title = input("* Question(" + str(question_number) + ") title: ")
                    if len(quiz_question_title) > 0:
                        break
                choice_number = 1
                print("* Question(" + str(question_number) + ") choices:-")
                print("  Note: When done adding choices, type \"correct\" to enter the correct answer's # and finish the question.")
                question_number += 1
                while True:
                    choice = input("Choice (" + str(choice_number) + "): ")
                    if len(choice) == 0:
                        continue
                    elif choice == "correct":
                        if choice_number < 3:
                            print("Please add at least two choices before entering \"correct\"")
                            continue
                        else:
                            while True:
                                correct_choice = input("* Correct choice #: ")
                                if len(choice) == 0:
                                    continue
                                else:
                                    quiz_questions.append({"title": quiz_question_title, "choices": quiz_question_choices, "correct_choice": correct_choice})
                                    break
                        break
                    else:
                        quiz_question_choices.append(choice)
                        choice_number += 1
            elif option == "save":
                if question_number < 2:
                    print("Quiz must have at least one question. Please add at least one question before entering \"save\"")
                    continue
                else:
                    database.add_quiz(quiz_name, quiz_subject, current_user["auth_cred"]["name"], quiz_questions)
                    print("------------------------------------------------------------------------------------")
                    return
            elif option == "discard":
                print("Discarding current quiz...")
                return
            else:
                print("Invalid option (" + option + "). Tip: Type \"discard\" to discard the form.")


def enter_admin_portal(database, current_user):
    print("-----------------------------------------------------------------------------------------")
    print("Welcome to the Admin portal, " + current_user["auth_cred"]["name"] + '.')
    print("-----------------------------------------")
    while True:
        print("You are in the Main Menu.")
        print("Available options: \"view\" to list all quizzes, \"add\" to create a quiz, or \"logout\" to save and exit:-")
        option = input("* Enter option: ")
        if option == "view":
            print_quizzes_list(database)
        elif option == "add":
            print_add_quiz_form(database, current_user)
        elif option == "logout":
            print("--------------")
            print("Logging out...")
            database.save_to_file()
            print("Successfully saved data to database. Goodbye.")
            print("----------------------------------------------")
            break
        else:
            print("Invalid option (" + option + "). Tip: Type \"quit\" to exit.")
            continue


def enter_student_portal(current_user):
    print("user portal")
    pass


def create_database_instance():
    return Database.instance()


def main():
    print_welcome_prompt()
    database = create_database_instance()
    database.load_from_file()
    current_user = authenticate(database)
    if current_user["auth_cred"]["role"] == Authenticator.ROLES["admin"]:
        enter_admin_portal(database, current_user)
    elif current_user["auth_cred"]["role"] == Authenticator.ROLES["student"]:
        enter_student_portal(current_user)


if __name__ == "__main__":
    main()
