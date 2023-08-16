import os

import utils.utilities
from utils import constants, definitions
from utils.utilities import InputVerificationUtils
from models.database import Database


def print_welcome_prompt():
    print("-" * 37)
    print("Welcome to this Quiz Program Portal.")
    print("Today's date & time is: " + utils.utilities.DateAndTime.get_date_and_time())
    print("-" * 74)


def create_database_instance():
    return Database.instance()


def authenticate(database):
    print("Please authenticate to get started.")
    while True:
        print("Available options::-\n" + str(definitions.LoginMenuItems.LOGIN.value) + ". Login\n" + str(definitions.LoginMenuItems.REGISTER.value) + ". Register\n" + str(definitions.LoginMenuItems.QUIT.value) + ". Quit")
        choice = input("* Your choice: ")
        if choice.lower() == str(definitions.LoginMenuItems.REGISTER.value):
            attempts = 3
            while True:
                print("Available account types:-\n" + str(definitions.Roles.ADMIN.value) + ". Admin\n" + str(definitions.Roles.STUDENT.value) + ". Student")
                account_type = input("* Your choice: ")
                if len(account_type) > 0:
                    break
            role = definitions.Roles.UNCLASSIFIED.value
            if account_type == str(definitions.Roles.STUDENT.value):
                role = definitions.Roles.STUDENT.value
            elif account_type == str(definitions.Roles.ADMIN.value):
                while True:
                    secret = input("* Enter the secret obtained from your network admin: ")
                    if secret != os.getenv('QUIZ_APP_ADMIN_SECRET'):
                        attempts -= 1
                        print("Wrong secret entered. You have " + str(attempts) + "/3 attempts left.")
                        if attempts == 0:
                            print("You ran out of attempts. Proceed to create a regular account and contact your network admin to be promoted later.")
                            break
                        continue
                    else:
                        role = definitions.Roles.ADMIN.value
                        break
            print("Create a new username & password:-")
            while True:
                user_name = input("* Enter username: ")
                if len(user_name) > 0:
                    break
            while True:
                user_password = input("* Enter password: ")
                if len(user_password) > 0:
                    break
            current_user = database.get_user_object().add_user(user_name, user_password, role)
            database.save_to_file()
            print("Registered successfully.")
            return current_user
        elif choice.lower() == str(definitions.LoginMenuItems.LOGIN.value):
            attempts = 3
            while True:
                user_name = input("* Enter username: ")
                if len(user_name) > 0:
                    break
            while True:
                user_password = input("* Enter password: ")
                if len(user_password) == 0:
                    continue
                else:
                    current_user = database.get_user_object().fetch_user(user_name, user_password)
                    if current_user is None:
                        attempts -= 1
                        print("Wrong credentials entered. You have " + str(attempts) + "/3 attempts left.")
                        if attempts == 0:
                            break
                        continue
                    else:
                        print("Logged in successfully.")
                        return current_user
        elif choice.lower() == str(definitions.LoginMenuItems.QUIT.value):
            print("No changes made. Quitting...")
            exit(0)
        else:
            print("Invalid option (" + choice + "). Tip: enter " + str(definitions.LoginMenuItems.QUIT.value) + " to quit.")


def enter_admin_portal(database, current_user):
    print("-" * 89)
    print("Welcome to the Admin portal, " + current_user["auth_cred"]["name"] + '.')
    print("-" * 41)
    while True:
        print("-" * 25)
        print("You are in the Main Menu.")
        print("Available options:-\n" + str(definitions.AdminMainMenuItems.VIEW_ALL_QUIZZES.value) + ". View all quizzes\n" + str(definitions.AdminMainMenuItems.CREATE_QUIZ.value) + ". Create a quiz\n" + str(definitions.AdminMainMenuItems.LOGOUT.value) + ". Logout")
        option = input("* Enter option: ")
        if option == str(definitions.AdminMainMenuItems.VIEW_ALL_QUIZZES.value):
            print_quizzes_list(database)
        elif option == str(definitions.AdminMainMenuItems.CREATE_QUIZ.value):
            print_add_quiz_form(database, current_user)
        elif option == str(definitions.AdminMainMenuItems.LOGOUT.value):
            print("-" * 14)
            print("Logging out...")
            database.save_to_file()
            print("Successfully saved data to database. Goodbye.")
            print("-" * 46)
            break
        else:
            print("Invalid option (" + option + "). Tip: Type " + str(definitions.AdminMainMenuItems.LOGOUT.value) + " to quit.")
            continue


def print_quiz(quiz):
    print("-" * 44)
    print("Taking quiz with ID (" + str(quiz["id"]) + "):-")
    print("-" * 44)
    print("- Quiz name: " + quiz["name"], ", ID: " + str(quiz["id"]) + ", Creator: " + quiz["owner_name"] + "\n")
    question_number = 1
    for question in quiz["questions"]:
        print("Question(" + str(question_number) + "): " + question["title"])
        question_number += 1
        choice_number = 1
        for choice in question["choices"]:
            print(str(choice_number) + ") " + choice)
            choice_number += 1
        print()
        answer = input("* Answer: ")
        if not InputVerificationUtils.isinteger(question["answer"]):
            print("There was an error reading the correct answer for this question (" + question["title"] + ") from the database. Please contact your data provider for a fix.")
        else:
            correct_answer = int(question["answer"]) + 1
            if answer == str(correct_answer):
                print("Correct! The answer is (" + question["choices"][correct_answer - 1] + ").")
            else:
                print("Incorrect! The answer is (" + question["choices"][correct_answer - 1] + ").")
        print("-" * 36)


def print_take_quiz_form(database):
    quizzes = database.get_quiz_object().fetch_all_quizzes()
    print("-" * 60)
    if len(quizzes) == 0:
        print("No quizzes exist in the database. To get started, a quiz has to be added.")
        print("-" * 60)
        return
    while True:
        print("Tip: type \"main menu\" to go to the main menu.")
        quiz_id = input("* Quiz ID: ")
        if len(quiz_id) == 0:
            continue
        elif quiz_id == "main menu":
            return
        else:
            quiz = database.get_quiz_object().fetch_quiz(quiz_id)
            if quiz is None:
                print("Quiz with this ID (" + quiz_id + ") does not exist. Please double check and try again.")
            else:
                print_quiz(quiz)


def enter_student_portal(database, current_user):
    print("-" * 89)
    print("Welcome to the Student portal, " + current_user["auth_cred"]["name"] + '.')
    print("-" * 41)
    while True:
        print("You are in the Main Menu.")
        print("Available options:-\n" + str(definitions.StudentMainMenuItems.VIEW_ALL_QUIZZES.value) + ". View all quizzes\n" + str(definitions.StudentMainMenuItems.TAKE_QUIZ.value) + ". Take a quiz using quiz ID\n" + str(definitions.StudentMainMenuItems.LOGOUT.value) + ". Logout")
        option = input("* Enter option: ")
        if option == str(definitions.StudentMainMenuItems.VIEW_ALL_QUIZZES.value):
            print_quizzes_list(database)
        elif option == str(definitions.StudentMainMenuItems.TAKE_QUIZ.value):
            print_take_quiz_form(database)
        elif option == str(definitions.StudentMainMenuItems.LOGOUT.value):
            print("-" * 14)
            print("Logging out...")
            database.save_to_file()
            print("Successfully saved data to database. Goodbye.")
            print("-" * 46)
            break
        else:
            print("Invalid option (" + option + "). Tip: Type " + str(definitions.StudentMainMenuItems.LOGOUT.value) + " to quit.")
            continue


def print_quizzes_list(database):
    quizzes = database.get_quiz_object().fetch_all_quizzes()
    print("-" * 60)
    if len(quizzes) == 0:
        print("No quizzes exist in the database. To get started, a quiz has to be added.")
        print("-" * 60)
        return
    print("Viewing all quizzes:-")
    print("-" * 21)
    for quiz in quizzes.values():
        print("- Quiz name: " + quiz["name"], ", ID: " + str(quiz["id"]) + ", Creator: " + quiz["owner_name"] + "\n")
        question_number = 1
        for question in quiz["questions"]:
            print("Question(" + str(question_number) + "): " + question["title"])
            question_number += 1
            choice_number = 1
            for choice in question["choices"]:
                print(str(choice_number) + ") " + choice)
                choice_number += 1
            print()
        print("-" * 36)


def print_add_quiz_form(database, current_user):
    while True:
        print("-" * 26)
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
            print("-" * 35)
            print("Available options for quiz (" + quiz_name + "):-\n" + str(definitions.AddQuizMenuItems.ADD_QUESTION.value) + ". Add a question\n" + str(definitions.AddQuizMenuItems.FINALIZE_AND_SAVE.value) + ". Finalize & Save\n" + str(definitions.AddQuizMenuItems.DISCARD.value) + ". Discard")
            option = input("* Option: ")
            if option == str(definitions.AddQuizMenuItems.ADD_QUESTION.value):
                quiz_question_choices = []
                while True:
                    quiz_question_title = input("* Question(" + str(question_number) + "): ")
                    if len(quiz_question_title) > 0:
                        break
                choice_number = 1
                print("* Question(" + str(question_number) + ") choices:-")
                print("  Note: When done adding choices, type \"correct\" to enter the correct answer's # and finalize the question.")
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
                                answer = input("* Correct choice #: ")
                                if len(choice) == 0:
                                    continue
                                elif not InputVerificationUtils.isinteger(answer):
                                    print("Answer must be a number representing the correct choice. Please try again.")
                                else:
                                    quiz_questions.append({"title": quiz_question_title, "choices": quiz_question_choices, "answer": int(answer) - 1})
                                    break
                        break
                    else:
                        quiz_question_choices.append(choice)
                        choice_number += 1
            elif option == str(definitions.AddQuizMenuItems.FINALIZE_AND_SAVE.value):
                if question_number < 2:
                    print("Quiz must have at least one question. Please add at least one question before finalizing.")
                    continue
                else:
                    database.get_quiz_object().add_quiz(quiz_name, quiz_subject, current_user["auth_cred"]["name"], quiz_questions)
                    database.save_to_file()
                    print("Quiz added successfully.")
                    print("-" * 84)
                    return
            elif option == str(definitions.AddQuizMenuItems.DISCARD.value):
                print("Discarding current quiz...")
                return
            else:
                print("Invalid option (" + option + "). Tip: Type " + str(definitions.AddQuizMenuItems.DISCARD.value) + " to discard the form and go to the main menu.")


def enter_unclassified_portal(database):
    print("This portal is for unclassified users. Nothing has been made available for you.")
    print("Logging out...")
    database.save_to_file()
    print("Successfully saved data to database. Goodbye.")
    exit(0)


def load_env_variables():
    import os
    try:
        env_file = open(constants.ENV_FILE_LOCATION, 'r')
        lines = env_file.readlines()
        for line in lines:
            key_value = line.split('=')
            os.environ[key_value[0]] = key_value[1]
    except FileNotFoundError:
        return


def main():
    print_welcome_prompt()
    load_env_variables()
    database = create_database_instance()
    database.load_from_file()
    current_user = authenticate(database)
    if current_user["auth_cred"]["role"] == definitions.Roles.ADMIN.value:
        enter_admin_portal(database, current_user)
    elif current_user["auth_cred"]["role"] == definitions.Roles.STUDENT.value:
        enter_student_portal(database, current_user)
    elif current_user["auth_cred"]["role"] == definitions.Roles.UNCLASSIFIED.value:
        enter_unclassified_portal(database)


if __name__ == "__main__":
    main()
