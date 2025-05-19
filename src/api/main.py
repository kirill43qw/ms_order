import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infra.message_broker.handlers import ItemValidHanlder
from src.infra.message_broker.consumer import RabbitMQConsumer
from src.infra.message_broker.base import RabbitMQ
from src.api.basket.routers import router as basket_router
from src.api.order.routers import router as order_router
from src.api.order.routers import admin_router as admin_router
from src.settings.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbitmq = RabbitMQ(settings.RABBITMQ_URL)
    consumer = RabbitMQConsumer(rabbitmq)
    item_handler = ItemValidHanlder()
    asyncio.create_task(
        consumer.consume_events(
            exchange_name="order_exchange",
            queue_name="valid_dishes",
            routing_key="dish.is_valid",
            message_handler=item_handler,
        )
    )
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(order_router)
app.include_router(basket_router)
app.include_router(admin_router)


@app.get("/hello")
async def hello():
    return {"message": "!!!!!!!check_router"}
