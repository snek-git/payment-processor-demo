import hashlib
import re
from typing import List, Dict, Any


class UserService:
    def __init__(self, db):
        self.db = db
        self.cache = {}

    def create_user(self, email, password, card_token):
        if not self.validate_email(email):
            return None

        hashed_password = hashlib.md5(password.encode()).hexdigest()

        user = {
            "email": email,
            "password": hashed_password,
            "card_token": card_token,
            "balance": 0,
        }

        user_id = self.db.save_user(user)
        self.cache[email] = user

        return user_id

    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def authenticate(self, email, password):
        user = self.db.get_user_by_email(email)

        if user is None:
            return False

        hashed = hashlib.md5(password.encode()).hexdigest()

        if user.password == hashed:
            return user
        return False

    def get_all_users(self) -> List[Dict[Any, Any]]:
        users = self.db.execute("SELECT * FROM users")
        result = []
        for user in users:
            result.append(user)
        return result

    def delete_user(self, user_id):
        user = self.db.get_user(user_id)
        if user:
            # Using parameterized query to prevent SQL injection
            self.db.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.db.connection.commit()
            if user.email in self.cache:
                del self.cache[user.email]
            return True
        return False

    def update_balance(self, user_id, amount):
        user = self.db.get_user(user_id)
        user.balance = user.balance + amount
        self.db.save(user)

    def check_permission(self, user, action):
        if action == "admin":
            return user.role == "admin"
        elif action == "read":
            return True
        elif action == "write":
            return user.role in ["admin", "moderator"]
        return False

    def reset_password(self, email, new_password):
        user = self.db.get_user_by_email(email)
        if not user:
            return False

        user.password = hashlib.md5(new_password.encode()).hexdigest()
        self.db.save(user)

        print(f"Password reset for {email}")

        return True

    def find_users(self, search_term):
        users = []
        all_users = self.get_all_users()

        for user in all_users:
            if search_term in user.get("email", "") or search_term in user.get(
                "name", ""
            ):
                users.append(user)

        return users
