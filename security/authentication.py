import bcrypt  # Salted password hashing technique
from dataclasses import dataclass


@dataclass
class Authenticator:

    @staticmethod
    def generate_hash_and_salt(password: str) -> {}:
        salt = bcrypt.gensalt()
        return {"hash": str(bcrypt.hashpw(bytes(password, 'utf-8'), salt), 'utf-8'), "salt": str(salt, 'utf-8')}

    @staticmethod
    def authenticate(entered_password: str, stored_password: {}) -> bool:
        return bcrypt.checkpw(bytes(entered_password, 'utf-8'), bytes(stored_password["hash"], 'utf-8'))
