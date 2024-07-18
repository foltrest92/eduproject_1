from fastapi import APIRouter

from app.api.users.dao import UsersDAO
from app.api.users.schemas import SUser, SUserBase

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/get')
async def get_users() -> list[SUser]:
    return await UsersDAO.find_all()

@router.post('/new')
async def reg_user(user: SUserBase) -> SUser:
    new_user = await UsersDAO.add(user)
    return new_user

@router.put('/update/{user_id}')
async def update_user(user: SUserBase, user_id: int) -> SUser:
    updated_user = await UsersDAO.update(user_id, user)
    return updated_user

@router.delete('/delete/{user_id}')
async def delete_user(user_id: int) -> bool:
    return await UsersDAO.delete(user_id)
