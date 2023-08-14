from models.quiz_entities import Quiz
from models.user_credentials import UserCredential
from models.user_entities import User, Admin, Student
import json
from dataclasses import dataclass
import CONSTANTS


@dataclass
class Database:
    _instance = None
    users = {}
    quizzes = {}

    def __init__(self):
        raise RuntimeError("Call Database's instance() method instead.")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def load_from_file(self):
        import os
        if not os.path.exists(CONSTANTS.DB_LOCATION_ON_DISK):
            return
        with open(CONSTANTS.DB_LOCATION_ON_DISK, 'r') as input_file:
            input_dictionary = json.load(input_file)
            print(input_dictionary)

    @classmethod
    def add_user(cls, user_name, user_password, user_role):
        user_credential = UserCredential(user_name, user_password, user_role)
        if user_role == UserCredential.ROLES["admin"]:
            cls.users[user_name] = Admin(user_credential)
        elif user_role == UserCredential.ROLES["student"]:
            cls.users[user_name] = Student(user_credential)
        return cls.users[user_name]

    @classmethod
    def fetch_user(cls, user_name, user_password) -> User:
        if user_name not in cls.users:
            return None
        user = cls.users[user_name]
        user_credentials = user.get_credentials()

        if UserCredential.authenticate(user_password, user_credentials.get_password_hash(),
                                       user_credentials.get_password_salt()):
            return user

    @classmethod
    def add_quiz(cls, quiz_name, quiz_subject, quiz_questions) -> Quiz:
        quiz_id = len(cls.quizzes)
        cls.quizzes[quiz_id] = Quiz(quiz_id, quiz_name, quiz_subject, quiz_questions)
        return cls.quizzes[quiz_id]

    @classmethod
    def fetch_quiz(cls, quiz_id) -> Quiz:
        if quiz_id in cls.quizzes:
            return cls.quizzes[quiz_id]
        else:
            return None

    @classmethod
    def fetch_all_quizzes(cls) -> {}:
        return cls.quizzes

    def __dict__(self):
        return {"users": {k: v.__dict__() for (k, v) in self.users.items()},
                "quizzes": {k: v.__dict__() for (k, v) in self.quizzes.items()}}

    def save_to_file(self):
        output_json = json.dumps(self.__dict__(), indent=2)
        with open(CONSTANTS.DB_LOCATION_ON_DISK, 'w') as output_file:
            output_file.write(output_json)
