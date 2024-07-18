from fastapi import APIRouter, Depends

from app.api.accounts.dao import AccountsDAO
from app.api.accounts.schemas import SAccount
from app.api.auth.permission import get_user_id, is_admin_permission

router = APIRouter(
    prefix='/accounts',
    tags=['Accounts']
)

@router.get('/get/my')
async def get_my_account(user_id = Depends(get_user_id)) -> list[SAccount]:
    account = await AccountsDAO.get_by_user(user_id)
    return account

@router.get('/get/{user_id}')
async def get_account_by_user(user_id: int, perm = Depends(is_admin_permission)) -> list[SAccount]:
    account = await AccountsDAO.get_by_user(user_id)
    return account
