from helpers.quiz import Quiz
from helpers.user import User
from utils import utilities
from security.authentication import Authenticator
import json
from dataclasses import dataclass
import constants


@dataclass
class Database:
    _instance = None
    userObject = None
    quizObject = None

    def __init__(self):
        raise RuntimeError("Call Database's instance() method instead.")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def load_from_file(self):
        self.userObject = User.instance()
        self.quizObject = Quiz.instance()
        import os
        if not os.path.exists(constants.DB_LOCATION_ON_DISK):
            return
        try:
            input_file = open(constants.DB_LOCATION_ON_DISK, 'r')
            input_dictionary = json.load(input_file)
            self.userObject.dict_from_list(input_dictionary["users"])
            self.quizObject.dict_from_list(input_dictionary["quizzes"])
            input_file.close()
        except KeyError:
            return

    def save_to_file(self):
        output_json = json.dumps(self.__dict__(), indent=2)
        with open(constants.DB_LOCATION_ON_DISK, 'w') as output_file:
            output_file.write(output_json)

    def __dict__(self) -> {}:
        return {"users": self.userObject.__dict__(), "quizzes": self.quizObject.__dict__()}

    def get_user_object(self):
        return self.userObject

    def get_quiz_object(self):
        return self.quizObject
