class PaymentAPI:
    def charge(self, card_token, amount):
        # Charges the card
        return PaymentResult("txn_123", True, amount)


class PaymentResult:
    def __init__(self, id, success, amount):
        self.id = id
        self.success = success
        self.amount = amount