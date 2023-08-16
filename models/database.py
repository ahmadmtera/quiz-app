from helpers.quiz import Quiz
from helpers.user import User
from utils import constants
import json
from dataclasses import dataclass


@dataclass
class Database:
    _instance = None
    user_object = None
    quiz_object = None

    def __init__(self):
        raise RuntimeError("Call Database's instance() method instead.")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def load_from_file(self) -> None:
        self.user_object = User.instance()
        self.quiz_object = Quiz.instance()
        import os
        if not os.path.exists(constants.DB_LOCATION_ON_DISK):
            return
        try:
            input_file = open(constants.DB_LOCATION_ON_DISK, 'r')
            input_dictionary = json.load(input_file)
            self.user_object.dict_from_list(input_dictionary["users"])
            self.quiz_object.dict_from_list(input_dictionary["quizzes"])
            input_file.close()
        except KeyError:
            return

    def save_to_file(self) -> None:
        output_json = json.dumps(self.__dict__(), indent=2)
        with open(constants.DB_LOCATION_ON_DISK, 'w') as output_file:
            output_file.write(output_json)

    def __dict__(self) -> {}:
        return {"users": [self.user_object.__dict__()], "quizzes": [self.quiz_object.__dict__()]}

    def get_user_object(self) -> User:
        return self.user_object

    def get_quiz_object(self) -> Quiz:
        return self.quiz_object
