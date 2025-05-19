from datetime import datetime
from typing import AsyncIterator
from sqlalchemy import Integer, func
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, class_mapper, mapped_column

from src.settings.config import settings


engine = create_async_engine(settings.DB_URL, echo=True)
async_sesion_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_sesssion() -> AsyncIterator[AsyncSession]:
    async with async_sesion_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
        finally:
            await session.close()


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    def to_dict(self) -> dict:
        """Универсальный метод для конвертации объекта SQLAlchemy в словарь"""
        columns = class_mapper(self.__class__).columns
        return {column.key: getattr(self, column.key) for column in columns}
