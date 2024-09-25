from user_statistics import UserStatistics
import bcrypt
from database_connection import *

class User:
    def __init__(self, name, email, password, cpf, is_active=True):
        self.name = name
        self.email = email
        self.password = self.hash_password(password) if isinstance(password, str) else password
        self.cpf = cpf
        self.is_active = is_active
        self.statistics = UserStatistics()

    @staticmethod
    def hash_password(password):
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def verify_password(self, password):
        # Check if the provided password matches the stored hash
        stored_password = self.password.encode('utf-8') if isinstance(self.password, str) else self.password
        return bcrypt.checkpw(password.encode('utf-8'), stored_password)

    def deactivate_account(self):
        self.is_active = False
        update_user_in_db(self)

    def reactivate_account(self):
        self.is_active = True
        update_user_in_db(self)

    def update_email(self, new_email):
        self.email = new_email
        update_user_in_db(self)

    def update_password(self, new_password):
        self.password = self.hash_password(new_password)
        update_user_in_db(self)

    def __str__(self):
        return f"User: {self.name}, Email: {self.email}, CPF: {self.cpf}, Active: {bool(self.is_active)}"


