"""
Module 1: Authentication and User Account Management Service
Part of PyCommerce Open-Source Engine
"""
import re


class UserManager:
    def __init__(self):
        self.users = {}
        self.failed_attempts = {}
        self.locked_accounts = set()

    def validate_username(self, username: str) -> bool:
        """
        Validates username rules:
        - Must be alphanumeric (underscores allowed)
        - Length must be between 3 and 20 characters (inclusive)
        """
        if not isinstance(username, str):
            return False
        if len(username) < 3 or len(username) > 20:
            return False
        return bool(re.match(r"^[a-zA-Z0-9_]+$", username))

    def validate_password(self, password: str) -> bool:
        """
        Validates password complexity:
        - Length must be between 8 and 32 characters (inclusive)
        - Must contain at least one digit
        - Must contain at least one uppercase letter
        - Must contain at least one special character (!@#$%^&*()-_)
        """
        if not isinstance(password, str):
            return False
        if len(password) < 8 or len(password) > 32:
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[!@#$%^&*()\-_]", password):
            return False
        return True

    def validate_email(self, email: str) -> bool:
        """
        Validates email address format:
        - Standard email regex pattern
        """
        if not isinstance(email, str):
            return False
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email))

    def validate_age(self, age: int) -> bool:
        """
        Validates user age eligibility:
        - Must be an integer between 18 and 100 (inclusive)
        """
        if not isinstance(age, int) or isinstance(age, bool):
            return False
        return 18 <= age <= 100

    def register_user(self, username: str, email: str, password: str, age: int) -> dict:
        """
        Registers a new user after full validation.
        """
        if not self.validate_username(username):
            raise ValueError("Invalid username. Must be 3-20 alphanumeric characters.")
        if username in self.users:
            raise ValueError("Username already exists.")
        if not self.validate_email(email):
            raise ValueError("Invalid email format.")
        if not self.validate_password(password):
            raise ValueError("Password does not meet complexity requirements.")
        if not self.validate_age(age):
            raise ValueError("Age must be between 18 and 100.")

        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "age": age,
            "is_active": True
        }
        self.users[username] = user_data
        self.failed_attempts[username] = 0
        return {"status": "SUCCESS", "username": username}

    def authenticate(self, username: str, password: str) -> bool:
        """
        Authenticates user with lockout protection (locks after 3 failed attempts).
        """
        if username in self.locked_accounts:
            raise PermissionError("Account is locked due to too many failed attempts.")
        if username not in self.users:
            return False

        if self.users[username]["password"] == password:
            self.failed_attempts[username] = 0
            return True
        else:
            self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
            if self.failed_attempts[username] >= 3:
                self.locked_accounts.add(username)
            return False
