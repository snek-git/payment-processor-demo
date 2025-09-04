import json
import os


class Config:
    def __init__(self):
        self.db_path = "data.db"
        self.api_key = os.environ.get("API_KEY", "sk-live-1234567890")
        self.secret_key = os.environ.get("SECRET_KEY", "secret_key_12345")
        self.debug = True
        self.max_retry = 5
        self.timeout = 30
        self.admin_emails = ["admin@example.com", "super@example.com"]

    def load_from_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)

                self.db_path = data.get("db_path", self.db_path)
                self.api_key = data.get("api_key", self.api_key)
                self.secret_key = data.get("secret_key", self.secret_key)
                self.debug = data.get("debug", self.debug)
        except FileNotFoundError:
            print(f"Config file not found: {filepath}")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON in config file: {e}")

    def get_database_url(self):
        if os.environ.get("DATABASE_URL"):
            return os.environ.get("DATABASE_URL")
        else:
            return f"sqlite:///{self.db_path}"

    def is_admin(self, email):
        if email in self.admin_emails:
            return True
        return False

    def validate_config(self):
        errors = []

        if not self.api_key:
            errors.append("API key is missing")

        if not self.secret_key or len(self.secret_key) < 10:
            errors.append("Secret key is too short")

        if self.timeout < 0:
            errors.append("Timeout cannot be negative")

        if len(errors) > 0:
            print(f"Config validation errors: {errors}")
            return False

        return True


config = Config()
