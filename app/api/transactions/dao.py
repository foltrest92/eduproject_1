from app.api.accounts.dao import AccountsDAO
from app.api.accounts.schemas import SAccount
from app.api.transactions.model import Transactions
from app.api.transactions.schemas import STransaction, STransactionBase
from app.dao.base import BaseDAO
from app.exceptions import InvalidSignatureException, TransactionIsAlreadyCommitedException
import hashlib
from app.config import settings

class TransactionsDAO(BaseDAO):
    model = Transactions
    uid = Transactions.transaction_id

    @classmethod
    async def commit(cls, transaction_new: STransaction) -> bool:
        if not cls.__check_signature(transaction_new):
            raise InvalidSignatureException
        if await cls.find_one_or_none(transaction_id=transaction_new.transaction_id):
            raise TransactionIsAlreadyCommitedException
        else:
            account = await AccountsDAO.find_all(
                user_id=transaction_new.user_id,
                account_id=transaction_new.account_id)
            if not account:
                await AccountsDAO.add(SAccount(
                    user_id=transaction_new.user_id,
                    account_id=transaction_new.account_id,
                    balance=0
                ))
            transaction = await super().add(**{
                'transaction_id': transaction_new.transaction_id,
                'user_id': transaction_new.user_id,
                'account_id': transaction_new.account_id,
                'amount': transaction_new.amount
            })
            return bool(transaction)
    
    @classmethod
    def __check_signature(cls, transaction: STransaction) -> bool:
        unhashed = f'{transaction.account_id}{transaction.amount}{transaction.transaction_id}{transaction.user_id}'
        unhashed += settings.PAYMENTS_SECRET_KEY
        hash = hashlib.sha256(unhashed.encode()).hexdigest()
        print(hash)
        return transaction.signature == hash

    @classmethod
    async def get_by_user(cls, user_id: int) -> list[STransactionBase]:
        return await cls.find_all(user_id=user_id)