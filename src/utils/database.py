"""Database module for payment processing."""


class Database:
    """Database operations handler."""

    def save(self, user):
        """Save user to database."""
        pass

    def save_transaction(self, user_id, amount, payment_id):
        """Record transaction in database."""
        pass


class User:
    """User model."""

    def __init__(self, user_id, email, balance, card_token):
        self.id = user_id
        self.email = email
        self.balance = balance
        self.card_token = card_token
