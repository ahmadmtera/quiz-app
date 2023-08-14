from abc import ABC, abstractmethod


class User(ABC):

    @abstractmethod
    def __init__(self, user_credentials):
        self.user_credentials = user_credentials

    def get_credentials(self):
        return self.user_credentials


class Student(User):

    def __init__(self, user_credentials):
        super().__init__(user_credentials)


class Admin(User):

    def __init__(self, user_credentials):
        super().__init__(user_credentials)
