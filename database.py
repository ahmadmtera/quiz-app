from models.user_credentials import UserCredential
from models.user_entities import User, Admin, Student
from threading import Lock


class DatabaseMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        # When the program is launched, there's no Singleton instance yet. Yet, multiple threads can simultaneously pass
        # this point. To make sure only one succeeds in creating an instance, the lock exists as a spinlock for any but
        # the first thread.
        with cls._lock:
            # The first thread to acquire the lock enters here.
            if cls not in cls._instances:
                # The first thread to acquire the lock succeeds to enter here too.
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        # After the first thread leaves the "with" block, the lock is lifted and other threads can enter the "with" block.
        # But since (cls is in cls._instances), the "if" statement body is not entered by any subsequent threads.
        return cls._instances[cls]


# Singleton class design pattern
class Database(metaclass=DatabaseMeta):

    people = {}

    @classmethod
    def add_user(cls, user_name, user_password, user_role):
        user_credential = UserCredential(user_name, user_password, user_role)
        if user_role == UserCredential.ROLES["admin"]:
            cls.people[user_name] = Admin(user_credential)
        elif user_role == UserCredential.ROLES["student"]:
            cls.people[user_name] = Student(user_credential)
        return cls.people[user_name]

    @classmethod
    def fetch_user(cls, user_name, user_password) -> User:
        if user_name not in cls.people:
            return None
        user = cls.people[user_name]
        user_credentials = user.get_credentials()

        if UserCredential.authenticate(user_password, user_credentials.get_password_hash(), user_credentials.get_password_salt()):
            return user

    def __init__(self, value: str) -> None:
        self.value = value
