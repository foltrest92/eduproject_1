from fastapi import APIRouter, Depends

from app.api.auth.permission import get_user_id, is_admin_permission
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

@router.get('/get/my')
async def get_user_by_id(user_id = Depends(get_user_id)) -> SUser:
    user = await UsersDAO.find_by_id(user_id)
    return user

@router.get('/get/{user_id}')
async def get_user_by_id(user_id: int, perm = Depends(is_admin_permission)) -> SUser:
    user = await UsersDAO.find_by_id(user_id)
    return user

@router.post('/new')
async def reg_user(user: SNewUser) -> SUser:
    new_user = await UsersDAO.registate(user)
    return new_user

@router.put('/update/{user_id}')
async def update_user(user: SUpdateUser, user_id: int, perm = Depends(is_admin_permission)) -> SUser:
    updated_user = await UsersDAO.update(user_id, user)
    return updated_user

@router.delete('/delete/{user_id}')
async def delete_user(user_id: int, perm = Depends(is_admin_permission)) -> bool:
    is_deleted = await UsersDAO.delete(user_id)
    return is_deleted
