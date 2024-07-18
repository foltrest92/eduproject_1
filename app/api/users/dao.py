from app.api.auth.utils import get_hashed_password
from app.dao.base import BaseDAO
from app.exceptions import NoFoundException, UserIsAlreadyExist

from app.api.users.models import Users
from app.api.users.schemas import SNewUser, SUpdateUser, SUser, SUserBase

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
        if await super().delete(user_id):
            return True
        else:
            raise NoFoundException
