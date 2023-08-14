from abc import ABC
from dataclasses import dataclass


@dataclass
class User(ABC):

    def get_credentials(self):
        return self.user_credentials


@dataclass
class Student(User):

    def __init__(self, user_credentials: {}):
        self.user_credentials = user_credentials

    def __dict__(self):
        return {"user_credentials": self.user_credentials.__dict__()}


@dataclass
class Admin(User):

    def __init__(self, user_credentials):
        self.user_credentials= user_credentials

    def __dict__(self):
        return {"user_credentials": self.user_credentials.__dict__()}
