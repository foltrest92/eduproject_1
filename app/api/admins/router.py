from fastapi import APIRouter, Depends

from app.api.admins.dao import AdminsDAO
from app.api.admins.schemas import SAdmin, SNewAdmin, SUpdateAdmin
from app.api.auth.permission import is_admin_permission

router = APIRouter(
    prefix='/admins',
    tags=['Admins']
)

@router.get('/get')
async def get_admins(perm = Depends(is_admin_permission)) -> list[SAdmin]:
    admins = await AdminsDAO.find_all()
    return admins

@router.post('/new')
async def reg_admin(admin: SNewAdmin, perm = Depends(is_admin_permission)) -> SAdmin:
    new_admin = await AdminsDAO.registate(admin)
    return new_admin

@router.put('/update/{admin_id}')
async def update_admin(admin: SUpdateAdmin, admin_id: int, perm = Depends(is_admin_permission)) -> SAdmin:
    updated_admin = await AdminsDAO.update(admin_id, admin)
    return updated_admin

@router.delete('/delete/{admin_id}')
async def delete_admin(admin_id: int, perm = Depends(is_admin_permission)) -> bool:
    is_deleted = await AdminsDAO.delete(admin_id)
    return is_deleted
