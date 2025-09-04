import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.payment_processor import PaymentProcessor
from services.user_service import UserService
from utils.database import Database
from utils.email_service import EmailService
from api.payment_api import PaymentAPI
from models.order import Order, OrderProcessor
from utils.config import config

logging.basicConfig(level=logging.INFO)


def main():
    if not config.validate_config():
        print("Invalid configuration")
        return

    db = Database(config.db_path)
    email_service = EmailService()
    payment_api = PaymentAPI(config.api_key)

    payment_processor = PaymentProcessor(payment_api, email_service, db)
    user_service = UserService(db)
    order_processor = OrderProcessor(db, payment_processor)

    admin_email = "admin@example.com"
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")

    user_id = user_service.create_user(admin_email, admin_password, "tok_admin")

    if user_id:
        print(f"Created admin user with ID: {user_id}")

    test_user_id = user_service.create_user("test@example.com", "password", "tok_test")

    if test_user_id:
        user = db.get_user(test_user_id)
        user.balance = 100.0
        db.save(user)

        result = payment_processor.process_payment(user, 50.0)
        print(f"Payment result: {result}")

        if result["success"]:
            refund_result = payment_processor.process_refund(result["transaction"])
            print(f"Refund result: {refund_result}")

    order = Order(
        test_user_id,
        [
            {"name": "Item 1", "price": 10.0, "quantity": 2},
            {"name": "Item 2", "price": 15.0, "quantity": 1},
        ],
    )

    order_result = order_processor.process_order(order)
    print(f"Order result: {order_result}")

    all_users = user_service.get_all_users()
    print(f"Total users: {len(all_users)}")

    for user_data in all_users:
        print(f"User: {user_data}")

    db.close()


if __name__ == "__main__":
    main()
