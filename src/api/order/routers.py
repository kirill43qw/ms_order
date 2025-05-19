from uuid import UUID
from fastapi import APIRouter, Request

from src.infra.database.models.order import OrderStatusEnum
from src.api.order.schemas import StatusEnum


router = APIRouter(prefix="/api/v1/orders", tags=["ORDERS"])
admin_router = APIRouter(prefix="/api/admin", tags=["ADMIN"])


# only owner; with filters
@router.get("")
async def get_orders_history(
    request: Request, status_enum: OrderStatusEnum | None = None
):
    pass


# owner or admin
@router.get("{order_id}")
async def get_order_by_id(request: Request, order_id: UUID):
    pass


# only admin or moderator
@router.patch("{order_id}/status")
async def change_status_for_order(request: Request):
    pass


@admin_router.get("/orders")
async def get_all_orders_with_filters():
    pass


@admin_router.get("/users/{users_id}/orders")
async def get_all_user_orders():
    pass
