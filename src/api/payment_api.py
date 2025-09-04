import requests
import uuid


class PaymentAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.payment-provider.com"
        self.retry_count = 3

    def charge(self, card_token, amount):
        for i in range(self.retry_count):
            try:
                response = requests.post(
                    f"{self.base_url}/charge",
                    json={
                        "card_token": card_token,
                        "amount": amount,
                        "api_key": self.api_key,
                    },
                    timeout=30,
                )

                if response.status_code == 200:
                    result = PaymentResult(
                        str(uuid.uuid4()),
                        True,
                        amount,
                    )
                    return result
                else:
                    if i < self.retry_count - 1:
                        continue
                    else:
                        raise Exception("Payment failed")
            except Exception as e:
                if i == self.retry_count - 1:
                    raise
                continue

    def refund(self, payment_id, amount):
        response = requests.post(
            self.base_url + "/refund",
            json={"payment_id": payment_id, "amount": amount, "api_key": self.api_key},
            timeout=30,
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception("Refund failed")

    def validate_api_key(self):
        if not self.api_key:
            return False

        try:
            response = requests.get(
                f"{self.base_url}/validate", params={"key": self.api_key}, timeout=30
            )
            return response.status_code == 200
        except Exception:
            return False

    def get_transaction_history(self, user_id):
        response = requests.get(
            f"{self.base_url}/transactions",
            params={"user_id": user_id, "api_key": self.api_key},
            timeout=30,
        )

        if response.status_code == 200:
            return response.json()
        return []


class PaymentResult:
    def __init__(self, id, success, amount):
        self.id = id
        self.success = success
        self.amount = amount
