from utils import utilities
from security.authentication import Authenticator
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
        try:
            input_file = open(CONSTANTS.DB_LOCATION_ON_DISK, 'r')
            input_dictionary = json.load(input_file)
            self.users = input_dictionary["users"]
            self.quizzes = input_dictionary["quizzes"]
            print(input_dictionary)
        except KeyError:
            return

    def add_user(self, user_name, user_password, user_role):
        auth_cred = {"name": user_name, "password": Authenticator.generate_hash_and_salt(user_password), "role": user_role}
        self.users[user_name] = {"auth_cred": auth_cred}
        return self.users[user_name]

    def fetch_user(self, user_name, user_password):
        if user_name not in self.users.keys():
            return None
        user = self.users[user_name]
        if Authenticator.authenticate(user_password, user["auth_cred"]["password"]):
            return user

    def add_quiz(self, quiz_name, quiz_subject, owner_name, quiz_questions):
        quiz_id = len(self.quizzes)
        self.quizzes[quiz_id] = {"id": quiz_id, "name": quiz_name, "subject": quiz_subject, "questions": quiz_questions, "owner_name": owner_name, "date_time_added": utilities.DateAndTime.get_date_and_time()}
        return self.quizzes[quiz_id]

    def fetch_quiz(self, quiz_id):
        if quiz_id in self.quizzes:
            return self.quizzes[quiz_id]
        else:
            return None

    def fetch_all_quizzes(self) -> {}:
        return self.quizzes

    def __dict__(self) -> {}:
        return {"users": self.users, "quizzes": self.quizzes}

    def save_to_file(self):
        output_json = json.dumps(self.__dict__(), indent=2)
        with open(CONSTANTS.DB_LOCATION_ON_DISK, 'w') as output_file:
            output_file.write(output_json)
