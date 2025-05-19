import aio_pika
from aio_pika.abc import AbstractExchange
from aio_pika.pool import Pool


class RabbitMQ:
    def __init__(self, url: str):
        self.url = url
        self.connection_pool = Pool(self._get_connection, max_size=10)
        self.channel_pool = Pool(self._get_channel, max_size=10)

    async def _get_connection(self):
        return await aio_pika.connect_robust(self.url)

    async def _get_channel(self):
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()

    async def _get_exchange(self, channel, exchange_name: str) -> AbstractExchange:
        return await channel.declare_exchange(
            exchange_name,
            type=aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

    async def close(self):
        await self.connection_pool.close()
        await self.channel_pool.close()
