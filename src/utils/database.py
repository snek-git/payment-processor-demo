class Database:
    def save(self, user):
        # Saves user to database
        pass
    
    def save_transaction(self, user_id, amount, payment_id):
        # Records transaction
        pass


class User:
    def __init__(self, id, email, balance, card_token):
        self.id = id
        self.email = email
        self.balance = balance
        self.card_token = card_token