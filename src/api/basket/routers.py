import json
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.di import get_rabbitmq_producer
from src.infra.message_broker.producer import RabbitMQProducer
from src.infra.repositories.item_order_repository import ItemOrderDAO
from src.infra.repositories.order_repository import OrderDAO
from src.infra.database.sqlalchemy import get_db_sesssion
from src.api.basket.schemas import BusketSchema, ItemAddSchema


router = APIRouter(prefix="/api/v1/basket", tags=["BASKET"])


# @router.get("/check")
# async def check(session: AsyncSession = Depends(get_db_sesssion)):
#     orders = await OrderDAO.get_all(session)
#     return orders


# получить корзину пользователя со статусом basket
@router.get("")
async def get_basket(
    request: Request,
    session: AsyncSession = Depends(get_db_sesssion),
):
    user_id = request.headers.get("user_id")
    basket = await OrderDAO.get_by_status(session, user_id=1)
    rsp_data = BusketSchema.model_validate(basket)

    return rsp_data


@router.post("")
async def create_basket_or_added_item(
    request: Request,
    schema: ItemAddSchema | None = None,
    producer: RabbitMQProducer = Depends(get_rabbitmq_producer),
    session: AsyncSession = Depends(get_db_sesssion),
):
    user_id = request.headers.get("user_id")
    basket = await OrderDAO.get_or_create_basket(session, user_id=1)
    if schema:
        await ItemOrderDAO.add(session, order_id=basket.id, **schema.model_dump())

    await producer.publish_event(
        exchange_name="order_exchange",
        routing_key="order.validate_dish",
        message=json.dumps({"dish_id": schema.dish_id}),
    )

    rsp_data = BusketSchema.model_validate(basket)
    return rsp_data


# only owner
@router.patch("/{item_id}")
async def update_item_quantity(request: Request, item_id: int, quantity=Query()):
    pass


# only owner
@router.delete("/{item_id}")
async def delete_item_from_basket(request: Request, item_id: int):
    pass


# only owner; меняет статус на pending, если все данные по
@router.post("/checkout")
async def check_basket(request: Request):
    # Publishes order.created event
    pass


# можно не писать, тут просто permission проверяется
# получить корзину по id, имеет право только admin or manager
@router.get("/{basket_id}")
async def get_basket_by_id(request: Request, basket_id: int):
    pass
