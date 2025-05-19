from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.sqlalchemy import Base


T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: type[T]

    @classmethod
    async def add(cls, session: AsyncSession, **values) -> T:
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
            await session.refresh(new_instance)
        except SQLAlchemyError as e:
            await session.rollback()
            raise ValueError(f"Failed to create {cls.model.__name__}: {str(e)}")
        return new_instance

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int | UUID) -> T | None:
        try:
            return await session.get(cls.model, id)
        except SQLAlchemyError as e:
            print(f"некая ошибка: {e}")
            raise ValueError(f"Failed to fetch {cls.model.__name__}: {str(e)}")

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[T]:
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalars().all()

    # TODO: переписать на один запрос
    @classmethod
    async def update(cls, session: AsyncSession, id: int | UUID, **values) -> T | None:
        instance = await cls.get_by_id(session, id)
        if instance:
            for key, value in values.items():
                setattr(instance, key, value)
            session.add(instance)
            try:
                await session.commit()
                await session.refresh(instance)
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return instance
        return None

    # TODO: переписать на один запрос
    @classmethod
    async def delete(cls, session: AsyncSession, id: int) -> None:
        instance = await cls.get_by_id(session, id)
        if instance:
            try:
                await session.delete(instance)
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
        return

    # @classmethod
    # @asynccontextmanager
    # async def _session_scope(cls):
    #     async with async_session_maker() as session:
    #         try:
    #             yield session
    #             await session.commit()
    #         except Exception:
    #             await session.rollback()
    #             raise
    #
    # @classmethod
    # async def validate_dish(cls, dish_id: int) -> dict | None:
    #     async with cls._session_scope() as session:
    #         dish = await cls._get_by_id(session, dish_id)
    #         return {
    #             "id": dish.id,
    #             "name": dish.name,
    #             "price": float(dish.price)
    #         } if dish else None

    # @classmethod
    # async def get_by_id(cls, session: AsyncSession, id: int | UUID) -> T:
    #     query = select(cls.model).where(cls.model.id == id)
    #     try:
    #         result = await session.execute(query)
    #         # return result.scalars().first()
    #         return result.scalar_one_or_none()
    #     except SQLAlchemyError as e:
    #         print(f"ERRROROROR {e}")
    #         raise e
