import smtplib, ssl, keyring
from email.message import EmailMessage
from os import getenv
from dotenv import load_dotenv


class EmailSender:
    def __init__(self):
        load_dotenv()
        self.sender = getenv('EMAIL')
        self.msg = EmailMessage()
        self.msg['From'] = self.sender
        self.password = keyring.get_password("gmail", self.sender)
        if self.password is None:
            # password not saved in keyring
            self.password = input("Input your password for Gmail: ")
            keyring.set_password("gmail", self.sender, self.password)

    def send_mail(self, recipient, subject, message_content):
        self.msg['To'] = recipient
        self.msg.set_content(message_content)
        self.msg['Subject'] = subject

        smtp_server = "smtp.gmail.com"
        port = 465
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port=port, context=context) as server:
            server.login(self.sender, self.password)
            server.send_message(self.msg)
            # server.sendmail(sender_email, "arkadiusz.budkowski.dev@gmail.com", 'wow is wow as wonsz')
            server.close()
