from app.dao.base import BaseDAO

from app.api.accounts.models import Accounts
from app.api.accounts.schemas import SAccount

class AccountsDAO(BaseDAO):
    model = Accounts
    uid = Accounts.account_id

    @classmethod
    async def get_by_user(cls, user_id: int) -> list[Accounts]:
        accounts = await cls.find_all(user_id=user_id)
        return accounts

    @classmethod
    async def add(cls, account: SAccount) -> SAccount:
        account = await super().add(**account.model_dump())
        return account