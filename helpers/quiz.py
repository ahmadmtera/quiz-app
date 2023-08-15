from abc import ABC


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

    def set_quizzes(self, quizzes):
        self.quizzes = quizzes
        return self

    def get_quizzes(self):
        return self.quizzes
