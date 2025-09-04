import smtplib
from email.mime.text import MIMEText
import os


class EmailService:
    def __init__(self):
        self.smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = 587
        self.username = os.environ.get("EMAIL_USER")
        self.password = os.environ.get("EMAIL_PASS")

    def send(self, recipient, message):
        try:
            msg = MIMEText(message)
            msg["Subject"] = "Payment Notification"
            msg["From"] = self.username
            msg["To"] = recipient

            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)

            server.send_message(msg)
            server.quit()

            print(f"Email sent to {recipient}: {message}")

            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    def send_bulk(self, recipients, message):
        successful = []
        failed = []

        for recipient in recipients:
            if self.send(recipient, message):
                successful.append(recipient)
            else:
                failed.append(recipient)

        return {"successful": successful, "failed": failed}

    def validate_smtp_config(self):
        if not self.username or not self.password:
            return False

        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.quit()
            return True
        except:
            return False
