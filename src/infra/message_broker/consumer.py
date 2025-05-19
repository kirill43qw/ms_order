import aio_pika

from src.infra.message_broker.handlers import MessageHandler
from src.infra.message_broker.base import RabbitMQ


class RabbitMQConsumer:
    def __init__(self, rabbitmq: RabbitMQ):
        self.rabbitmq = rabbitmq

    async def consume_events(
        self,
        exchange_name: str,
        queue_name: str,
        routing_key: str,
        message_handler: MessageHandler,
    ):
        try:
            async with self.rabbitmq.connection_pool.acquire() as connection:
                channel = await connection.channel()
                exchange = await channel.declare_exchange(
                    exchange_name,
                    type=aio_pika.ExchangeType.TOPIC,
                    durable=True,
                )
                queue = await channel.declare_queue(queue_name, durable=True)
                await queue.bind(exchange, routing_key=routing_key)

                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        try:
                            async with message.process():
                                await message_handler(message)
                        except Exception as e:
                            print(f"error in processing message: {e}")
        except Exception as e:
            print(f"error in consume_events: {e}")
