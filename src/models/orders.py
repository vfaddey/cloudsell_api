import enum
import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, ForeignKey, Enum, DECIMAL, DateTime
from sqlalchemy.orm import relationship

from src.db.database import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    pricing_plan_id = Column(UUID(as_uuid=True), ForeignKey('pricing_plans.id'), nullable=False)
    server_id = Column(UUID(as_uuid=True), ForeignKey('servers.id'))
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    total_price = Column(DECIMAL, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    paid_at = Column(DateTime)

    server = relationship('Server', back_populates='order')
