from app.dao.base import BaseDAO
from app.exceptions import NoFoundException, UserIsAlreadyExist

from app.api.admins.models import Admins
from app.api.admins.schemas import SAdmin, SAdminBase

class AdminsDAO(BaseDAO):
    model = Admins
    uid = Admins.admin_id

    @classmethod
    async def find_all(cls) -> list[SAdmin]:
        return await super().find_all()

    @classmethod
    async def add(cls, admin_base: SAdminBase) -> SAdmin:
        if await cls.find_one_or_none(email=admin_base.email):
            raise UserIsAlreadyExist
        else:
            admin = await super().add(**admin_base.model_dump())
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
