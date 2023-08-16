from abc import ABC
from utils.utilities import DateAndTime, InputVerificationUtils


class Quiz(ABC):
    _instance = None
    quizzes = {}

    def __init__(self):
        raise RuntimeError("Call Quiz's instance() method instead.")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def add_quiz(self, quiz_name: str, quiz_subject: str, owner_name: str, quiz_questions: []) -> {}:
        quiz_id = len(self.quizzes)
        self.quizzes[quiz_id] = {"id": quiz_id, "name": quiz_name, "subject": quiz_subject, "questions": quiz_questions,
                                 "owner_name": owner_name, "date_time_added": DateAndTime.get_date_and_time()}
        return self.quizzes[quiz_id]

    def fetch_quiz(self, quiz_id: int) -> {}:
        if quiz_id not in self.quizzes.keys():
            return None
        else:
            return self.quizzes[quiz_id]

    def fetch_all_quizzes(self) -> {}:
        return self.quizzes

    def dict_from_list(self, quizzes: []) -> {}:
        resultant_dict = {}
        for key, value in quizzes[0].items():
            resultant_dict[key] = value
        self.quizzes = resultant_dict

    def __dict__(self) -> {}:
        return self.quizzes
