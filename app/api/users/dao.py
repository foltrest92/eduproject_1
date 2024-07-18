from app.dao.base import BaseDAO
from app.exceptions import NoFoundException, UserIsAlreadyExist

from app.api.users.models import Users
from app.api.users.schemas import SUser, SUserBase

class UsersDAO(BaseDAO):
    model = Users
    uid = Users.user_id

    @classmethod
    async def find_all(cls) -> list[SUser]:
        result = await super().select()
        return result

    @classmethod
    async def registate(cls, user_base: SUserBase) -> SUser:
        if await cls.select_one_or_none(email=user_base.email):
            raise UserIsAlreadyExist
        else:
            user = await super().insert(**user_base.model_dump())
            return user
    
    @classmethod
    async def update(cls, user_id: int, user_base: SUserBase) -> SUser:
        updated_user = await super().update(user_id, **user_base.model_dump())
        return updated_user
    
    @classmethod
    async def delete(cls, user_id: int) -> bool:
        if await super().delete(user_id):
            return True
        else:
            raise NoFoundException
