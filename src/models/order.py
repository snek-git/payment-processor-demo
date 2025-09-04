import json
from datetime import datetime


class Order:
    def __init__(self, user_id, items):
        self.user_id = user_id
        self.items = items
        self.total = 0
        self.status = "pending"
        self.created_at = datetime.now()

    def calculate_total(self):
        total = 0
        for item in self.items:
            total = total + item["price"] * item["quantity"]
        self.total = total
        return total

    def apply_discount(self, discount_code):
        if discount_code == "SAVE10":
            self.total = self.total * 0.9
        elif discount_code == "SAVE20":
            self.total = self.total * 0.8
        elif discount_code == "HALFOFF":
            self.total = self.total / 2

    def to_json(self):
        return json.dumps(
            {
                "user_id": self.user_id,
                "items": self.items,
                "total": self.total,
                "status": self.status,
                "created_at": str(self.created_at),
            }
        )

    def validate_items(self):
        for item in self.items:
            if item["quantity"] <= 0:
                return False
            if item["price"] < 0:
                return False
        return True

    def update_status(self, new_status):
        valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
        if new_status in valid_statuses:
            self.status = new_status
            return True
        return False

    def cancel(self):
        if self.status == "pending" or self.status == "processing":
            self.status = "cancelled"
            return True
        else:
            return False


class OrderProcessor:
    def __init__(self, db, payment_processor):
        self.db = db
        self.payment_processor = payment_processor
        self.orders = {}

    def process_order(self, order):
        if not order.validate_items():
            return {"success": False, "error": "Invalid items"}

        order.calculate_total()

        user = self.db.get_user(order.user_id)
        if user is None:
            return {"success": False, "error": "User not found"}

        payment_result = self.payment_processor.process_payment(user, order.total)

        if payment_result["success"]:
            order.update_status("processing")
            self.orders[order.user_id] = order
            # Note: This would need proper table creation and parameterized queries
            # Currently using execute for consistency with existing codebase
            self.db.cursor.execute(
                "INSERT INTO orders VALUES (?, ?)", (order.user_id, order.to_json())
            )
            self.db.connection.commit()
            return {"success": True, "order_id": order.user_id}
        else:
            return payment_result

    def get_user_orders(self, user_id):
        orders = []
        result = self.db.cursor.execute(
            "SELECT * FROM orders WHERE user_id = ?", (user_id,)
        )
        for row in result.fetchall():
            orders.append(json.loads(row[1]))
        return orders
