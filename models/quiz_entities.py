from datetime import datetime

from utilities import InputVerificationUtils


class Quiz:
    def __init__(self, quiz_id, quiz_name, quiz_questions, quiz_subject):
        if not InputVerificationUtils.isinteger(quiz_id):
            raise ValueError("Age must be an integer in __self__ method of the Quiz class.")
        self.quiz_id = quiz_id
        self.quiz_name = quiz_name
        self.quiz_questions = quiz_questions
        self.quiz_subject = quiz_subject
        self.date_time_added = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


class QuizQuestion:
    def __init__(self, name, question_choices):
        self.name = name
        self.question_choices = question_choices
