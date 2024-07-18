from fastapi import APIRouter, Depends

from app.api.auth.permission import is_admin_permission
from app.api.transactions.dao import TransactionsDAO
from app.api.transactions.schemas import STransaction, STransactionBase

router = APIRouter(
    prefix='/transactions',
    tags=['Transactions']
)

@router.post('/commit')
async def commit(transaction: STransaction) -> bool:
    result = await TransactionsDAO.commit(transaction)
    return result

@router.get('/get/my')
async def get_my_accounts():
    pass

@router.get('/get/{user_id}')
async def get_accounts(user_id: int, perm = Depends(is_admin_permission)) -> list[STransactionBase]:
    result = await TransactionsDAO.get_by_user(user_id)
    return result
