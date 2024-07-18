import hashlib

from sqlalchemy import and_, insert, update, union

from app.api.accounts.models import Accounts
from app.dao.base import BaseDAO
from app.exceptions import InvalidSignatureException, TransactionIsAlreadyCommitedException
from app.config import settings

from app.api.accounts.dao import AccountsDAO
from app.api.accounts.schemas import SAccount
from app.api.transactions.model import Transactions
from app.api.transactions.schemas import STransaction, STransactionBase

class TransactionsDAO(BaseDAO):
    model = Transactions
    uid = Transactions.transaction_id

    @classmethod
    async def commit(cls, transaction_new: STransaction) -> bool:
        if not cls.__check_signature(transaction_new):
            raise InvalidSignatureException
        if await cls.select_one_or_none(transaction_id=transaction_new.transaction_id):
            raise TransactionIsAlreadyCommitedException
        account = await AccountsDAO.select(
                user_id=transaction_new.user_id,
                account_id=transaction_new.account_id)
        if not account:
            account = await AccountsDAO.new(SAccount(
                    user_id=transaction_new.user_id,
                    account_id=transaction_new.account_id
                ))
        d_transaction = insert(Transactions).values(
            transaction_id= transaction_new.transaction_id,
            user_id= transaction_new.user_id,
            account_id= transaction_new.account_id,
            amount= transaction_new.amount
        ).returning(Transactions)
        d_balance = update(Accounts).where(and_(
                Accounts.user_id == transaction_new.user_id,
                Accounts.account_id == transaction_new.account_id
            )).values(balance = account.balance).returning(Accounts)
        query = [d_transaction, d_balance]
        result = await cls._update_base(query)
        return bool(result)
    
    @classmethod
    def __check_signature(cls, transaction: STransaction) -> bool:
        unhashed = f'{transaction.account_id}{transaction.amount}{transaction.transaction_id}{transaction.user_id}'
        unhashed += settings.PAYMENTS_SECRET_KEY
        hash = hashlib.sha256(unhashed.encode()).hexdigest()
        print(hash)
        return transaction.signature == hash

    @classmethod
    async def get_by_user(cls, user_id: int) -> list[STransactionBase]:
        result = await cls.select(user_id=user_id)
        return result
