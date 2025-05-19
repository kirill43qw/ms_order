from datetime import datetime, timezone
import aio_pika
from src.infra.message_broker.base import RabbitMQ
from src.settings.config import settings


class RabbitMQProducer:
    def __init__(self, rabbitmq: RabbitMQ):
        self.rabbitmq = rabbitmq
        self.service_name = settings.SERVICE_NAME
        self.api_key = settings.API_KEY

    async def publish_event(
        self,
        exchange_name: str,
        routing_key: str,
        message: str,
    ):
        async with self.rabbitmq.channel_pool.acquire() as channel:
            exchange = await self.rabbitmq._get_exchange(channel, exchange_name)
            await exchange.publish(
                aio_pika.Message(
                    body=message.encode(),
                    headers={
                        "service_name": self.service_name,
                        "api_key": self.api_key,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    },
                ),
                routing_key=routing_key,
            )
