from models.user_entities import User
import bcrypt  # Salted password hashing technique


class UserCredential:
    ROLES = {"admin": 0, "student": 1}

    def __init__(self, username, password, role) -> None:
        self.username = username
        self.password_salt = self.generate_salt()
        self.password_hash = self.generate_hash(password, self.password_salt)
        if role not in self.ROLES.values():
            raise ValueError(
                "The role code passed to __init__ of UserCredential is invalid. Please refer to the valid entries and try again.")
        self.role = role

    @staticmethod
    def generate_salt():
        return bcrypt.gensalt()

    @staticmethod
    def generate_hash(password, salt) -> bytes:
        return bcrypt.hashpw(str(password).encode('utf-8'), salt)

    @staticmethod
    def authenticate(password, stored_hash, stored_salt):
        return bcrypt.checkpw(password, stored_hash + stored_salt)

    def get_username(self) -> str:
        return self.username

    def get_password_hash(self) -> str:
        return self.password_hash

    def get_password_salt(self) -> str:
        return self.password_salt

    def get_role(self) -> str:
        return self.role
