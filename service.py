import json
from dataclasses import dataclass

import aio_pika

from client import MailClient
from core.config import settings
from schemas import UserMessageBody


@dataclass
class MailService:
    mail_client: MailClient

    async def consume_mail(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process():
            email_body = UserMessageBody(**json.loads(message.body.decode()))
            correlation_id = message.correlation_id
            print(f"Received message: {email_body}")
            try:
                self.send_email(
                    subject=email_body.subject, text=email_body.message, to=email_body.user_email
                )
            except Exception as e:
                await self.send_mail_fail_callback(
                    email=email_body.user_email, correlation_id=correlation_id, exception=e
                )

    @staticmethod
    async def send_mail_fail_callback(email: str, correlation_id: str, exception: Exception) -> None:
        from utils import get_amqp_connection

        connection = await get_amqp_connection()
        async with connection.channel() as channel:
            await channel.default_exchange.publish(
                message=aio_pika.Message(
                    body=f"Sending mail to {email} failed with exception: {exception}".encode(),
                    correlation_id=correlation_id,
                ),
                routing_key=settings.broker.callback_mail_queue,
            )

    def send_email(self, subject, text, to):
        self.mail_client.send_email_task(subject, text, to)
