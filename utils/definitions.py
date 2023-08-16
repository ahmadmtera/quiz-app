from enum import Enum


class Roles(Enum):
    UNCLASSIFIED: int = 0
    ADMIN: int = 1
    STUDENT: int = 2


class LoginMenuItems(Enum):
    LOGIN: int = 1
    REGISTER: int = 2
    QUIT: int = 3


class AdminMainMenuItems(Enum):
    VIEW_ALL_QUIZZES: int = 1
    CREATE_QUIZ: int = 2
    LOGOUT: int = 3


class StudentMainMenuItems(Enum):
    VIEW_ALL_QUIZZES: int = 1
    TAKE_QUIZ: int = 2
    LOGOUT: int = 3


class AddQuizMenuItems(Enum):
    ADD_QUESTION: int = 1
    FINALIZE_AND_SAVE: int = 2
    DISCARD: int = 3
