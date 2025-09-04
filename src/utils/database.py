import sqlite3
import json


class Database:
    def __init__(self, db_path="data.db"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.init_tables()

    def init_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                email TEXT,
                password TEXT,
                card_token TEXT,
                balance REAL,
                role TEXT,
                is_active INTEGER
            )
        """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                amount REAL,
                payment_id TEXT,
                timestamp INTEGER
            )
        """
        )

        self.connection.commit()

    def execute(self, query):
        result = self.cursor.execute(query)
        self.connection.commit()
        return result.fetchall()

    def save_user(self, user_data):
        query = """
            INSERT INTO users (email, password, card_token, balance, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(
            query,
            (
                user_data["email"],
                user_data["password"],
                user_data["card_token"],
                user_data.get("balance", 0),
                user_data.get("role", "user"),
                user_data.get("is_active", 1),
            ),
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_user(self, user_id):
        result = self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = result.fetchone()
        if user:
            return User(user[0], user[1], user[2], user[3], user[4], user[5], user[6])
        return None

    def get_user_by_email(self, email):
        result = self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = result.fetchone()
        if user:
            return User(user[0], user[1], user[2], user[3], user[4], user[5], user[6])
        return None

    def save(self, obj):
        if isinstance(obj, User):
            query = """
                UPDATE users 
                SET balance = ?, 
                    is_active = ?,
                    password = ?
                WHERE id = ?
            """
            self.cursor.execute(
                query, (obj.balance, obj.is_active, obj.password, obj.id)
            )
            self.connection.commit()

    def save_transaction(self, user_id, amount, payment_id):
        import time

        query = """
            INSERT INTO transactions (user_id, amount, payment_id, timestamp)
            VALUES (?, ?, ?, ?)
        """
        self.cursor.execute(query, (user_id, amount, payment_id, int(time.time())))
        self.connection.commit()

    def get_transaction(self, transaction_id):
        result = self.cursor.execute(
            "SELECT * FROM transactions WHERE id = ?", (transaction_id,)
        )
        transaction = result.fetchone()
        if transaction:
            return Transaction(
                transaction[0], transaction[1], transaction[2], transaction[3]
            )
        return None

    def close(self):
        self.connection.close()

    def __del__(self):
        try:
            self.connection.close()
        except:
            pass


class User:
    def __init__(self, id, email, password, card_token, balance, role, is_active):
        self.id = id
        self.email = email
        self.password = password
        self.card_token = card_token
        self.balance = balance
        self.role = role
        self.is_active = is_active


class Transaction:
    def __init__(self, id, user_id, amount, payment_id):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.payment_id = payment_id
