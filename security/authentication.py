import bcrypt  # Salted password hashing technique
from dataclasses import dataclass


@dataclass
class Authenticator:
    ROLES = {"admin": 0, "student": 1, "unclassified": 2}

    @staticmethod
    def generate_hash_and_salt(password) -> {}:
        salt = bcrypt.gensalt()
        return {"hash": str(bcrypt.hashpw(bytes(password, 'utf-8'), salt), 'utf-8'), "salt": str(salt, 'utf-8')}

    @staticmethod
    def authenticate(entered_password, stored_password: {}):
        return bcrypt.checkpw(bytes(entered_password, 'utf-8'), bytes(stored_password["hash"], 'utf-8'))
