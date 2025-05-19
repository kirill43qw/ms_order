from src.infra.message_broker.base import RabbitMQ
from src.infra.message_broker.consumer import RabbitMQConsumer
from src.infra.message_broker.producer import RabbitMQProducer


# RABBITMQ_URL = "amqp://guest:guest@localhost/"
RABBITMQ_URL = "amqp://guest:guest@rabbitmq/"


rabbitmq = RabbitMQ(RABBITMQ_URL)
producer = RabbitMQProducer(rabbitmq)


async def get_rabbitmq_producer() -> RabbitMQProducer:
    return producer


async def get_rabbitmq_consumer() -> RabbitMQConsumer:
    return RabbitMQConsumer(rabbitmq)
