import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, ForeignKey, Enum, DateTime, Float
from sqlalchemy.orm import relationship

from src.db.database import Base


class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    SERVER_PAYMENT = "server_payment"


class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    CANCELLED = "cancelled"
    SUCCESS = "success"


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey('wallets.id'), nullable=False, index=True)
    status = Column(Enum(TransactionStatus), nullable=False, default=TransactionStatus.PENDING)
    amount = Column(Float(asdecimal=True), nullable=False, default=0)
    transaction_type = Column(Enum(TransactionType), nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    wallet = relationship("Wallet", back_populates="transactions")

