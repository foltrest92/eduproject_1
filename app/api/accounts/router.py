from fastapi import APIRouter

from app.api.accounts.dao import AccountsDAO

router = APIRouter(
    prefix='/accounts',
    tags=['Accounts']
)

@router.get('/get/my')
async def get_my_account():
    pass

@router.get('/get/{user_id}')
async def get_account_by_user(user_id: int):
    return await AccountsDAO.get_by_user(user_id)

