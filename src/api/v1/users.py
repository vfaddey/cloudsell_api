from fastapi import APIRouter, Depends

from src.api.deps import get_current_user
from src.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.get('/me',
            response_model=UserOut,
            description='Данные пользователя')
async def get_me(user: UserOut = Depends(get_current_user)):
    return user
