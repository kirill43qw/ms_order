from sqlalchemy import select
from sqlalchemy.orm.strategy_options import selectinload
from src.infra.database.models.order_item import OrderItem
from src.infra.database.models.order import Order, OrderStatusEnum
from src.infra.repositories.base_repository import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession


class OrderDAO(BaseDAO):
    model = Order
    item_model = OrderItem

    @classmethod
    async def get_by_status(
        cls, session: AsyncSession, user_id: int, status: str = OrderStatusEnum.BASKET
    ) -> Order | list[Order]:
        # selectinload и так настроен в модели, это просто для наглядности
        query = (
            select(cls.model)
            .filter_by(user_id=user_id, status=status)
            .options(selectinload(cls.model.items))
        )
        result = await session.execute(query)
        # переписать на all(), потому что нельзя будет получить история заказов
        return result.scalar_one_or_none()

    @classmethod
    async def get_or_create_basket(cls, session: AsyncSession, user_id: int) -> Order:
        result = await session.execute(
            select(cls.model).where(
                (cls.model.user_id == user_id)
                & (cls.model.status == OrderStatusEnum.BASKET)
            )
        )
        basket = result.scalar_one_or_none()
        if not basket:
            basket = await cls.add(session, user_id=user_id)
        return basket
