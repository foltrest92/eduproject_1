from sqlalchemy import delete
from app.api.admins.models import Admins
from app.api.admins.schemas import SAdmin, SNewAdmin, SUpdateAdmin
from app.api.auth.model import JWTAdminTokens
from app.api.auth.utils import get_hashed_password
from app.dao.base import BaseDAO
from app.exceptions import NoFoundException, UserIsAlreadyExist

class AdminsDAO(BaseDAO):
    model = Admins
    uid = Admins.admin_id

    @classmethod
    async def find_all(cls) -> list[SAdmin]:
        result = await super().select()
        return result

    @classmethod
    async def registate(cls, admin_base: SNewAdmin) -> SAdmin:
        if await cls.select_one_or_none(email=admin_base.email):
            raise UserIsAlreadyExist
        else:
            hashed_password = get_hashed_password(admin_base.password)
            admin = await super().insert(**{
                'email':admin_base.email,
                'full_name':admin_base.full_name,
                'hashed_password': hashed_password
            })
            return admin
    
    @classmethod
    async def update(cls, admin_id: int, admin_update: SUpdateAdmin) -> SAdmin:
        update_data = admin_update.model_dump()
        update_data = {k:v for k, v in update_data.items() if v is not None}
        if 'password' in update_data:
            update_data['hashed_password'] = get_hashed_password(update_data['password'])
            del(update_data['password'])
        updated_admin = await super().update(admin_id, **update_data)
        return updated_admin
    
    @classmethod
    async def delete(cls, admin_id: int) -> bool:
        if await super().delete(admin_id):
            return True
        else:
            raise NoFoundException
    
    @classmethod
    async def delete(cls, admin_id: int) -> bool:
        delete_tokens_query = delete(JWTAdminTokens).where(JWTAdminTokens.admin_id == admin_id)
        delete_admin_query = delete(Admins).where(Admins.admin_id == admin_id)
        queries = [
            delete_tokens_query,
            delete_admin_query
            ]
        result = await cls._update_base(queries)
        if result[-1] == True:
            return True
        else:
            raise NoFoundException
