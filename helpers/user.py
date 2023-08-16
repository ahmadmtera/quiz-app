from abc import ABC
from security.authentication import Authenticator


class User(ABC):
    _instance = None
    users = {}

    def __init__(self):
        raise RuntimeError("Call User's instance() method instead.")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def add_user(self, user_name, user_password, user_role):
        auth_cred = {"name": user_name, "password": Authenticator.generate_hash_and_salt(user_password), "role": user_role}
        self.users[user_name] = {"auth_cred": auth_cred}
        return self.users[user_name]

    def fetch_user(self, user_name, user_password):
        if user_name not in self.users.keys():
            return None
        user = self.users[user_name]
        if Authenticator.authenticate(user_password, user["auth_cred"]["password"]):
            return user

    def dict_from_list(self, users):
        resultant_dict = {}
        for i in range(0, len(users)):
            resultant_dict[users[i]["auth_cred"]["name"]] = users[i]
        self.users = resultant_dict

    def __dict__(self):
        return list(self.users.values())
