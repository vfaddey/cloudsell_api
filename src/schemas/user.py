from decimal import Decimal

from black import datetime
from pydantic import BaseModel, EmailStr, condecimal
from pydantic import UUID4
from src.models import AccountType, Currency


class WalletOut(BaseModel):
    balance: Decimal
    updated_at: datetime

    class Config:
        from_attributes = True


class UserAdd(BaseModel):
    id: UUID4
    name: str
    email: EmailStr
    email_confirmed: bool
    account_type: AccountType
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserOut(UserAdd):
    is_admin: bool = False
    wallet: WalletOut

