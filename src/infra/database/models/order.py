import uuid
from decimal import Decimal
from enum import StrEnum
from sqlalchemy import Numeric, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.infra.database.sqlalchemy import Base
from src.settings.config import settings


class OrderStatusEnum(StrEnum):
    BASKET = "basket"
    PENDING = "pending"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": settings.DB_SCHEMA}
    # добавить CheckConstraint для total_amount?

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[int] = mapped_column(index=True)
    status: Mapped[OrderStatusEnum] = mapped_column(default=OrderStatusEnum.BASKET)
    total_amount: Mapped[Decimal] = mapped_column(  # как считать общую сумму?
        Numeric(precision=None, scale=2),
        default=0,
        nullable=False,
    )
    delivery_address: Mapped[str | None]

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
