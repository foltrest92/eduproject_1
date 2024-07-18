from fastapi import APIRouter, Depends

from app.api.accounts.dao import AccountsDAO
from app.api.auth.permission import is_admin_permission

router = APIRouter(
    prefix='/accounts',
    tags=['Accounts']
)

@router.get('/get/my')
async def get_my_account():
    pass

@router.get('/get/{user_id}')
async def get_account_by_user(user_id: int, perm = Depends(is_admin_permission)):
    account = await AccountsDAO.get_by_user(user_id)
    return account

