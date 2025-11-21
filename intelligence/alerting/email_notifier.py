import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotifier:
    def __init__(self, smtp_config):
        """
        smtp_config dict expects: server, port, email, password, recipient
        """
        self.config = smtp_config

    def send(self, subject, body):
        if not self.config:
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email']
            msg['To'] = self.config['recipient']
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.config['server'], self.config['port'])
            server.starttls()
            server.login(self.config['email'], self.config['password'])
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"[!] Email Send Error: {e}")