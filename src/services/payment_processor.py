"""Payment processor module."""

import logging

log = logging.getLogger(__name__)

class PaymentProcessor:
    """Handles payment processing logic."""

    def __init__(self, payment_api, email_service, db):
        self.payment_api = payment_api
        self.email = email_service
        self.db = db

    def process_payment(self, user, amount):
        """Process a payment for a user."""
        # Check user can afford it
        if user.balance >= amount:
            # Log the attempt
            log.info("Payment %s for user %s", amount, user.email)

            # Charge the payment
            result = self.payment_api.charge(user.card_token, amount)

            # Update user balance
            user.balance -= amount
            self.db.save(user)

            # Send confirmation
            self.email.send(user.email, f"Charged ${amount}")

            # Record transaction
            self.db.save_transaction(user.id, amount, result.id)

            return {"success": True, "transaction": result.id}

        return {"success": False, "error": "Insufficient funds"}

