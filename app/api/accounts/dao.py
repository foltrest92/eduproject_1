from app.dao.base import BaseDAO

from app.api.accounts.models import Accounts
from app.api.accounts.schemas import SAccount

class AccountsDAO(BaseDAO):
    model = Accounts
    uid = Accounts.account_id

    @classmethod
    async def get_by_user(cls, user_id: int) -> list[Accounts]:
        accounts = await cls.select(user_id=user_id)
        return accounts

    @classmethod
    async def new(cls, account: SAccount) -> SAccount:
        account = await super().insert(**account.model_dump())
        return account
    
    @classmethod
    async def select(cls, **filter_by) -> SAccount:
        result = await super().select_one_or_none(**filter_by)
        return result