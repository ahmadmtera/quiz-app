from datetime import datetime

from utilities import InputVerificationUtils


class Quiz:
    def __init__(self, quiz_id, quiz_name, quiz_subject, quiz_questions: []):
        if not InputVerificationUtils.isinteger(quiz_id):
            raise ValueError("Age must be an integer in __self__ method of the Quiz class.")
        self.quiz_id = quiz_id
        self.quiz_name = quiz_name
        self.quiz_subject = quiz_subject
        self.quiz_questions = quiz_questions
        self.date_time_added = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def get_id(self):
        return self.quiz_id

    def get_name(self):
        return self.quiz_name

    def get_subject(self):
        return self.quiz_subject

    def get_questions(self):
        return self.quiz_questions

    def get_date_time_added(self):
        return self.date_time_added


class QuizQuestion:
    def __init__(self, title, choices: []):
        self.title = title
        self.choices: [] = choices

    def get_title(self):
        return self.title

    def get_choices(self):
        return self.choices
