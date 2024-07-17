from uuid import UUID
from fastapi import APIRouter

from app.api.admins.dao import AdminsDAO
from app.api.admins.schemas import SAdmin, SAdminBase



router = APIRouter(
    prefix='/admins',
    tags=['Admins']
)

@router.get('/get')
async def get_admins() -> list[SAdmin]:
    return await AdminsDAO.find_all()

@router.post('/new')
async def new_admin(admin: SAdminBase) -> SAdmin:
    new_user = await AdminsDAO.add(admin)
    return new_admin

@router.put('/update/{admin_id}')
async def update_admin(admin: SAdminBase, admin_id: UUID) -> SAdmin:
    updated_admin = await AdminsDAO.update(admin_id, admin)
    return updated_admin

@router.delete('/delete/{admin_id}')
async def delete_admin(admin_id: UUID) -> bool:
    return await AdminsDAO.delete(admin_id)


