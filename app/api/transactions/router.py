from fastapi import APIRouter

from app.api.transactions.dao import TransactionsDAO
from app.api.transactions.schemas import STransaction, STransactionBase


router = APIRouter(
    prefix='/transactions',
    tags=['Transactions']
)

@router.post('/commit')
async def commit(transaction: STransaction) -> bool:
    return await TransactionsDAO.commit(transaction)

@router.get('/get/{user_id}')
async def get_accounts(user_id: int) -> list[STransactionBase]:
    return await TransactionsDAO.get_by_user(user_id)

