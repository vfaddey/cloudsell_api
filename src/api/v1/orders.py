from pydantic import UUID4
from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse

from src.api.deps import get_current_user, get_order_service
from src.exceptions.base import CloudSellAPIException
from src.exceptions.order import FailedToCreateOrder, OrderNotFound, NoAccessOrder
from src.schemas.order import OrderOut, OrderAdd
from src.schemas.user import UserOut
from src.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=OrderOut,
             description='Создание заказа')
async def create_order(order: OrderAdd,
                       user: UserOut = Depends(get_current_user),
                       order_service: OrderService = Depends(get_order_service)):
    try:
        result = await order_service.create(order, user.id)
        return result
    except FailedToCreateOrder as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except CloudSellAPIException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('',
            status_code=status.HTTP_200_OK,
            response_model=list[OrderOut],
            description='Получить все свои заказы')
async def get_by_user_id(user: UserOut = Depends(get_current_user),
                         order_service: OrderService = Depends(get_order_service)):
    result = await order_service.get_by_user_id(user.id)
    return result


@router.get('/{order_id}',
            status_code=status.HTTP_200_OK,
            response_model=OrderOut,
            description='Получить заказ по id (UUID)')
async def get_order(order_id: UUID4,
                    user: UserOut = Depends(get_current_user),
                    order_service: OrderService = Depends(get_order_service)):
    try:
        result = await order_service.get(order_id, user.id)
        return result
    except OrderNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NoAccessOrder as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except CloudSellAPIException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/{order_id}/pay')
async def get_pay_link(order_id: UUID4,
                       user: UserOut = Depends(get_current_user),
                       order_service: OrderService = Depends(get_order_service)):
    return {'pay_link': 'https:youtube.com'}


@router.post('/{order_id}/pay')
async def pay_order(order_id: UUID4,
                    order_service: OrderService = Depends(get_order_service)):
    try:
        result = await order_service.confirm_payment(order_id)
        return result
    except OrderNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CloudSellAPIException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))