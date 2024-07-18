from app.dao.base import BaseDAO
from app.exceptions import NoFoundException, UserIsAlreadyExist

from app.api.admins.models import Admins
from app.api.admins.schemas import SAdmin, SAdminBase

class AdminsDAO(BaseDAO):
    model = Admins
    uid = Admins.admin_id

    @classmethod
    async def find_all(cls) -> list[SAdmin]:
        return await cls.select()

    @classmethod
    async def registate(cls, admin_base: SAdminBase) -> SAdmin:
        if await cls.select_one_or_none(email=admin_base.email):
            raise UserIsAlreadyExist
        else:
            admin = await super().insert(**admin_base.model_dump())
            return admin
    
    @classmethod
    async def update(cls, admin_id: int, admin_base: SAdminBase) -> SAdmin:
        updated_admin = await super().update(admin_id, **admin_base.model_dump())
        return updated_admin
    
    @classmethod
    async def delete(cls, admin_id: int) -> bool:
        if await super().delete(admin_id):
            return True
        else:
            raise NoFoundException
