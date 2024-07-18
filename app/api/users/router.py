from fastapi import APIRouter, Depends

from app.api.auth.permission import is_admin_permission
from app.api.users.dao import UsersDAO
from app.api.users.schemas import SNewUser, SUpdateUser, SUser

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/get')
async def get_users(perm = Depends(is_admin_permission)) -> list[SUser]:
    users = await UsersDAO.find_all()
    return users

@router.post('/new')
async def reg_user(user: SNewUser) -> SUser:
    new_user = await UsersDAO.registate(user)
    return new_user

@router.put('/update/{user_id}')
async def update_user(user: SUpdateUser, user_id: int, perm = Depends(is_admin_permission)) -> SUser:
    updated_user = await UsersDAO.update(user_id, user)
    return updated_user

@router.delete('/delete/{user_id}', perm = Depends(is_admin_permission))
async def delete_user(user_id: int) -> bool:
    is_deleted = await UsersDAO.delete(user_id)
    return is_deleted
