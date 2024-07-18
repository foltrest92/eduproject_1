from fastapi import APIRouter

from app.api.users.dao import UsersDAO
from app.api.users.schemas import SNewUser, SUpdateUser, SUser

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/get')
async def get_users() -> list[SUser]:
    users = await UsersDAO.find_all()
    return users

@router.post('/new')
async def reg_user(user: SNewUser) -> SUser:
    new_user = await UsersDAO.registate(user)
    return new_user

@router.put('/update/{user_id}')
async def update_user(user: SUpdateUser, user_id: int) -> SUser:
    updated_user = await UsersDAO.update(user_id, user)
    return updated_user

@router.delete('/delete/{user_id}')
async def delete_user(user_id: int) -> bool:
    is_deleted = await UsersDAO.delete(user_id)
    return is_deleted
