import enum
import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, ForeignKey, JSON, String, Enum, DateTime
from sqlalchemy.orm import relationship

from src.db.database import Base


class ServerStatus(str, enum.Enum):
    WORKING = "working"
    STOPPED = "stopped"
    CANCELLED = "cancelled"


class Server(Base):
    __tablename__ = 'servers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey('providers.id'), nullable=False)
    pricing_plan_id = Column(UUID(as_uuid=True), ForeignKey('pricing_plans.id'), nullable=False, index=True)
    server_status = Column(Enum(ServerStatus), default=ServerStatus.STOPPED)
    additional_info = Column(JSON, default={})

    next_payment_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    pricing_plan = relationship('PricingPlan')
    provider = relationship('Provider')
    user = relationship('User', back_populates='servers')
    order = relationship('Order', back_populates='server')
