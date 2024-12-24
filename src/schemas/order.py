from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, UUID4

from src.models import OrderStatus


class OrderAdd(BaseModel):
    pricing_plan_id: UUID4

    class Config:
        from_attributes = True


class OrderOut(OrderAdd):
    id: UUID4
    status: OrderStatus
    total_price: Decimal
    created_at: datetime
    paid_at: Optional[datetime] = None
    server_id: Optional[UUID4] = None