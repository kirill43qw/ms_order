from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ItemSchema(BaseModel):
    dish_id: int | None
    dish_name: str | None
    unit_price: Decimal | None
    quantity: int | None

    model_config = ConfigDict(from_attributes=True)


class ItemAddSchema(BaseModel):
    dish_id: int
    quantity: int = Field(default=1, gt=0, le=10)


class BusketSchema(BaseModel):
    id: UUID
    user_id: int
    status: str
    total_amount: Decimal
    delivery_address: str | None
    created_at: datetime
    items: list[ItemSchema] | None

    model_config = ConfigDict(from_attributes=True)
