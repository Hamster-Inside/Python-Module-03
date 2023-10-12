import smtplib, ssl, keyring
from email.message import EmailMessage


class EmailSender:
    def __init__(self, port, smtp_server, credentials, ssl_enabled=False):
        self.port = port
        self.smtp_server = smtp_server
        self.credentials = credentials
        self.ssl_enabled = ssl_enabled

        self.msg = EmailMessage()
        self.msg['From'] = self.credentials.username
        self.password = keyring.get_password("gmail", self.credentials.username)
        if self.password is None:
            # password not saved in keyring
            # For manual input uncomment 2 lines below
            # self.password = input("Input your password for Gmail: ")
            # keyring.set_password("gmail", self.sender, self.password)

            # password from .env file
            keyring.set_password("gmail", self.credentials.username, self.credentials.password)

    def __enter__(self):
        if not self.ssl_enabled:
            self.connection = smtplib.SMTP(self.smtp_server, self.port)
        else:
            context = ssl.create_default_context()
            self.connection = smtplib.SMTP_SSL(self.smtp_server, self.port, context=context)

        self.connection.login(self.credentials.username, self.credentials.password)

        return self

    def send_mail(self, recipient, subject, message_content):
        self.msg['To'] = recipient
        self.msg.set_content(message_content)
        self.msg['Subject'] = subject

        self.connection.send_message(self.msg)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
