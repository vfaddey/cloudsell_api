import enum
import uuid
from datetime import datetime
from email.policy import default

from sqlalchemy import UUID, Column, String, Boolean, Enum, DateTime, ForeignKey, Float

from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship

from src.db.database import Base


class AccountType(enum.Enum):
    PHYSICAL = "physical"
    COMPANY = "company"


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(VARCHAR(70), unique=True, nullable=False)
    email_confirmed = Column(Boolean, default=False)
    account_type = Column(Enum(AccountType), default=AccountType.PHYSICAL)
    is_admin = Column(Boolean, default=False, nullable=False)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey('wallets.id'))

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False, onupdate=datetime.now)

    reviews = relationship('Review', back_populates='user')
    wallet = relationship('Wallet', back_populates='user', lazy='joined')
    servers = relationship('Server', back_populates='user')


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4(), primary_key=True, index=True, nullable=False)
    balance = Column(Float(asdecimal=True), nullable=False, default=0)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    transactions = relationship('Transaction', back_populates='wallet')
    user = relationship('User', back_populates='wallet')

