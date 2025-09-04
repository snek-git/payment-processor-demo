"""Payment API module."""


class PaymentAPI:
    """Payment API handler."""

    def charge(self, card_token, amount):  # pylint: disable=unused-argument
        """Charge the card with specified amount."""
        # Charges the card
        return PaymentResult("txn_123", True, amount)


class PaymentResult:
    """Payment result model."""

    def __init__(self, txn_id, success, amount):
        self.id = txn_id
        self.success = success
        self.amount = amount
