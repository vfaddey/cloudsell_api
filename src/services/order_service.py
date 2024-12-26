from uuid import UUID

from src.exceptions.order import OrderInsertFailed, OrderNotFound, FailedToCreateOrder, NoAccessOrder
from src.exceptions.pricing_plan import PricingPlanNotFound
from src.models import Order, OrderStatus
from src.repositories.order_repository import OrderRepository
from src.repositories.pricing_plan_repository import PricingPlanRepository
from src.schemas.order import OrderAdd, OrderOut


class OrderService:
    def __init__(self,
                 order_repository: OrderRepository,
                 pricing_plan_repository: PricingPlanRepository):
        self.__order_repository = order_repository
        self.__pricing_plan_repository = pricing_plan_repository

    async def create(self,
                     order: OrderAdd,
                     user_id: UUID) -> OrderOut:
        try:
            pricing_plan = await self.__pricing_plan_repository.get(order.pricing_plan_id)
            if not pricing_plan:
                raise PricingPlanNotFound(f'No pricing plan found with id {order.pricing_plan_id}')
            to_insert = Order(user_id=user_id,
                              pricing_plan_id=pricing_plan.id,
                              total_price=pricing_plan.price)
            inserted = await self.__order_repository.create(to_insert)
            return inserted
        except OrderInsertFailed as e:
            print(e)
            raise FailedToCreateOrder('Failed to create order')

    async def get(self, order_id: UUID, user_id: UUID) -> OrderOut:
        order = await self.__order_repository.get(order_id)
        if not order:
            raise OrderNotFound(f'Order with id {order_id} not found')
        if order.user_id != user_id:
            raise NoAccessOrder('You do not have access to this order')
        return OrderOut.from_orm(order)

    async def get_by_user_id(self, user_id: UUID) -> list[OrderOut]:
        orders = await self.__order_repository.get_by_user_id(user_id)
        return [OrderOut.from_orm(o) for o in orders]

    async def confirm_payment(self, order_id: UUID):
        try:
            order = await self.__order_repository.get(order_id)
            if not order:
                raise OrderNotFound(f'Order with id {order_id} not found')
            order.status = OrderStatus.COMPLETED
            result = await self.__order_repository.update(order)
            return OrderOut.from_orm(result)
        except OrderInsertFailed as e:
            print(e)
            raise FailedToCreateOrder('Failed to create order')

    async def update(self):
        ...

    async def delete(self, order_id: UUID):
        order = await self.__order_repository.delete(order_id)
        if not order:
            raise OrderNotFound(f'Order with id {order_id} not found')
        return OrderOut.from_orm(order)
