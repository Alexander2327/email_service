import smtplib
import ssl
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from core.config import settings


@dataclass
class MailClient:
    settings: settings

    def send_email_task(self, subject: str, text: str, to: str):
        msg = self._build_message(subject, text, to)
        self._send_email(msg=msg)

    def _build_message(self, subject: str, text: str, to: str) -> MIMEMultipart:
        msg = MIMEMultipart()

        msg["From"] = self.settings.mail.email_from
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(text, "plain"))
        return msg

    def _send_email(self, msg: MIMEMultipart):
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(
            self.settings.mail.host, self.settings.mail.port, context=context
        )
        server.login(self.settings.mail.user, self.settings.mail.password)
        server.send_message(msg)
        server.quit()
