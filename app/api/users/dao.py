from sqlalchemy import delete, select
from app.api.accounts.models import Accounts
from app.api.auth.model import JWTTokens
from app.api.auth.utils import get_hashed_password
from app.api.transactions.model import Transactions
from app.dao.base import BaseDAO
from app.exceptions import NoFoundException, UserIsAlreadyExist

from app.api.users.models import Users
from app.api.users.schemas import SNewUser, SUpdateUser, SUser

class UsersDAO(BaseDAO):
    model = Users
    uid = Users.user_id

    @classmethod
    async def find_all(cls) -> list[SUser]:
        result = await super().select()
        return result

    @classmethod
    async def registate(cls, user_base: SNewUser) -> SUser:
        if await cls.select_one_or_none(email=user_base.email):
            raise UserIsAlreadyExist
        else:
            hashed_password = get_hashed_password(user_base.password)
            user = await super().insert(**{
                'email':user_base.email,
                'full_name':user_base.full_name,
                'hashed_password': hashed_password
            })
            return user
        
    @classmethod
    async def find_by_id(cls, user_id):
        query = select(Users.__table__.columns).filter_by(user_id=user_id)
        result = await cls._select(query)
        mapped = result.mappings().one_or_none()
        if mapped:
            return mapped
        raise NoFoundException()

    @classmethod
    async def update(cls, user_id: int, user_update: SUpdateUser) -> SUser:
        update_data = user_update.model_dump()
        update_data = {k:v for k, v in update_data.items() if v is not None}
        if 'password' in update_data:
            update_data['hashed_password'] = get_hashed_password(update_data['password'])
            del(update_data['password'])
        updated_user = await super().update(user_id, **update_data)
        return updated_user
    
    @classmethod
    async def delete(cls, user_id: int) -> bool:
        delete_transactions_query = delete(Transactions).where(Transactions.user_id == user_id)
        delete_account_query = delete(Accounts).where(Accounts.user_id == user_id)
        delete_tokens_query = delete(JWTTokens).where(JWTTokens.user_id == user_id)
        delete_user_query = delete(Users).where(Users.user_id == user_id)
        queries = [delete_transactions_query,
                    delete_account_query,
                    delete_tokens_query,
                    delete_user_query]
        result = await cls._update_base(queries)
        if result[-1] == True:
            return True
        else:
            raise NoFoundException