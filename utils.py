import aio_pika

from client import MailClient
from service import MailService

from core.config import settings


async def get_mail_service() -> MailService:
    return MailService(
        mail_client=MailClient(settings=settings)
    )


async def get_amqp_connection() -> aio_pika.abc.AbstractConnection:
    return await aio_pika.connect_robust(settings.broker.url)


async def make_amqp_consumer():
    mail_service = await get_mail_service()
    connection = await get_amqp_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue(settings.broker.mail_queue, durable=True)
    await queue.consume(mail_service.consume_mail)