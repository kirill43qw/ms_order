from sqlalchemy import delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.sqlalchemy import async_sesion_maker
from src.infra.database.models.order_item import OrderItem
from src.infra.repositories.base_repository import BaseDAO


class ItemOrderDAO(BaseDAO):
    model = OrderItem

    @classmethod
    async def update_name_price_in_validate_item(cls, body: dict):
        # print(
        #     f"UPDATE: {body.get('dish_id')}, вот такие данные я добавлю в item {body}"
        # )
        async with async_sesion_maker() as session:
            try:
                stmt = (
                    update(cls.model)
                    .where(cls.model.dish_id == body["dish_id"])
                    .values(dish_name=body["dish_name"], unit_price=body["price"])
                )
                await session.execute(stmt)
                await session.commit()
            except SQLAlchemyError as er:
                await session.rollback()
                print("Что-то пошло не так при обновлении колонки")

    @classmethod
    async def delete_invalid_item(cls, dish_id: int):
        # print("DELETE: удалил невалидное блюдо в корзине")
        async with async_sesion_maker() as session:
            try:
                stmt = delete(cls.model).where(cls.model.dish_id == dish_id)
                await session.execute(stmt)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                print(f"не удалось удалить объект: {e}")
