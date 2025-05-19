from abc import ABC
import json

from aio_pika import IncomingMessage

from src.infra.repositories.item_order_repository import ItemOrderDAO


class MessageHandler(ABC):
    async def __call__(self, message: IncomingMessage): ...


class ItemValidHanlder(MessageHandler):
    async def __call__(self, message: IncomingMessage):
        service_name = message.headers.get("service_name")
        body = json.loads(message.body.decode())

        if body.get("is_valid"):
            await ItemOrderDAO.update_name_price_in_validate_item(body)
            return
        await ItemOrderDAO.delete_invalid_item(dish_id=body.get("dish_id"))
