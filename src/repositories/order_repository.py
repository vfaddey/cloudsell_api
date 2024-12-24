from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions.order import OrderInsertFailed
from src.models import Order


class OrderRepository(ABC):
    @abstractmethod
    def create(self, order):
        raise NotImplementedError

    @abstractmethod
    def get(self, order_id: int | UUID):
        raise NotImplementedError

    @abstractmethod
    def get_by_user_id(self, user_id: int | UUID):
        raise NotImplementedError

    @abstractmethod
    def update(self, order):
        raise NotImplementedError

    @abstractmethod
    def delete(self, order_id: int | UUID):
        raise NotImplementedError


class SqlaOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, order: Order):
        try:
            self._session.add(order)
            await self._session.commit()
            await self._session.refresh(order)
            return order
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise OrderInsertFailed(e)

    async def get(self, order_id: UUID) -> Order:
        stmt = select(Order).where(Order.id == order_id)
        result = await self._session.execute(stmt)
        return result.unique().scalar()

    async def get_by_user_id(self, user_id: UUID):
        stmt = select(Order).where(Order.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.unique().scalars().all()

    async def update(self, order):
        try:
            self._session.add(order)
            await self._session.commit()
            await self._session.refresh(order)
            return order
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise OrderInsertFailed(e)

    async def delete(self, order_id: UUID):
        stmt = delete(Order).where(Order.id == order_id).returning(Order)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.unique().scalars().first()
