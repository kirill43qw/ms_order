from pydantic import BaseModel, ConfigDict

from src.infra.database.models.order import OrderStatusEnum


class StatusEnum(BaseModel):
    # model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    status: OrderStatusEnum
