import uuid
from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.database.sqlalchemy import Base
from src.settings.config import settings


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = {"schema": settings.DB_SCHEMA}

    order_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ms_order.orders.id"),
        nullable=False,
    )
    # order_id: Mapped[int] = mapped_column(
    #     ForeignKey("ms_order.orders.id"),
    #     nullable=False,
    # )
    dish_id: Mapped[int] = mapped_column(index=True)
    dish_name: Mapped[str | None] = mapped_column(String(30))
    unit_price: Mapped[Decimal | None] = mapped_column(Numeric(precision=None, scale=2))
    quantity: Mapped[int] = mapped_column(default=1)

    order: Mapped["Order"] = relationship(back_populates="items")
