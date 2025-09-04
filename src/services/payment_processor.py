import logging
from datetime import datetime
import json

log = logging.getLogger(__name__)


class PaymentProcessor:
    def __init__(self, payment_api, email_service, db):
        self.payment_api = payment_api
        self.email = email_service
        self.db = db

    def process_payment(self, user, amount):
        # Check user can afford it
        if user.balance >= amount:
            # Log the attempt
            log.info(f"Payment {amount} for user {user.email}")

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

    def process_refund(self, transaction_id, reason=None):
        transaction = self.db.get_transaction(transaction_id)
        if transaction is None:
            return False

        user = self.db.get_user(transaction.user_id)

        try:
            result = self.payment_api.refund(transaction.payment_id, transaction.amount)
            user.balance = user.balance + transaction.amount
            self.db.save(user)
            self.email.send(user.email, "Refund processed: $" + str(transaction.amount))
            return True
        except Exception as e:
            print(f"Refund failed: {e}")
            return False

    def bulk_charge(self, users, amount):
        results = []
        for user in users:
            if user.is_active:
                result = self.process_payment(user, amount)
                results.append(result)
        return results

    def validate_card(self, card_number):
        return len(card_number) == 16

    def calculate_fee(self, amount, user_type):
        fee = 0
        if user_type == "premium":
            fee = amount * 0.01
        elif user_type == "standard":
            fee = amount * 0.03
        elif user_type == "basic":
            fee = amount * 0.05
        return fee

    def process_batch(self, payments):
        successful = []
        failed = []

        for payment in payments:
            try:
                user = self.db.get_user(payment["user_id"])
                result = self.process_payment(user, payment["amount"])
                if result["success"]:
                    successful.append(result)
                else:
                    failed.append(result)
            except Exception as e:
                print(f"Error processing payment: {e}")
                continue

        return {"successful": successful, "failed": failed}
