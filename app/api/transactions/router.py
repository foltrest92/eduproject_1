from fastapi import APIRouter

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

@router.get('/get/{user_id}')
async def get_accounts(user_id: int) -> list[STransactionBase]:
    result = await TransactionsDAO.get_by_user(user_id)
    return result
