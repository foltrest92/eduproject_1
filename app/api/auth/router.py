from fastapi import APIRouter, Response

from app.api.auth.dao import AuthDAO
from app.api.auth.schemas import EmailPassword, TokensPair
from app.config import settings

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/login')
async def login(response: Response, email_password: EmailPassword) -> TokensPair:
    tokens = await AuthDAO.auth(email_password)
    response.set_cookie(key='access_token',
                        value=tokens.access_token,
                        max_age=settings.ACCESS_TOKEN_AGE)
    
    response.set_cookie(key='refresh_token',
                        value=tokens.refresh_token,
                        httponly=True,
                        max_age=settings.REFRESH_TOKEN_AGE)
    return tokens

@router.post('/admin/login')
async def admin_login(response: Response, email_password: EmailPassword) -> TokensPair:
    tokens = await AuthDAO.auth(email_password, is_admin=True)
    response.set_cookie(key='access_token',
                        value=tokens.access_token,
                        max_age=settings.ACCESS_TOKEN_AGE)
    
    response.set_cookie(key='refresh_token',
                        value=tokens.refresh_token,
                        httponly=True,
                        max_age=settings.REFRESH_TOKEN_AGE)
    return tokens
