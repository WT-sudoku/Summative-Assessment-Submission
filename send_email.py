import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    '''
    A class responsible for sending emails.
    '''
    def __init__(self, sender_email, sender_password):
        '''
        Initialize the EmailSender instance with the sender's email and password.

        :param sender_email: The sender's email address.
        :param sender_password: The sender's app-specific password.
        '''
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, recipient_name, recipient_email, subject, body):
        '''
        Send an email to the Employee.

        :param recipient_name: The recipient's name.
        :param recipient_email: The recipient's email address.
        :param subject: The email subject.
        :param body: The email body.
        '''
        # Configure MIMEMultipart object
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        # Attach email body (Add body to email)
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
                # Log in to the email server (gmail)
                server.login(self.sender_email, self.sender_password)
                # Send email
                server.send_message(msg)
            print(f"Email sent to {recipient_name} at {recipient_email}")
        except Exception as e:
            print("Failed to send email.")
            print(e)


# Optional: Example usage for testing only
# def main():
#     sender_email = "your_email@gmail.com"
#     sender_app_password = "your_app_password"
#     email_sender = EmailSender(sender_email, sender_app_password)
#     email_sender.send_email(
#         "Test User",
#         "testuser@example.com",
#         "Test Subject",
#         "This is a test message."
#     )

# if __name__ == "__main__":
#     main()
