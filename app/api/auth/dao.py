from datetime import datetime, timedelta, timezone
import uuid

from sqlalchemy import delete, insert, select
from app.api.admins.models import Admins
from app.api.admins.schemas import SAdmin, SAdminBase, SAdminWithPassword
from app.api.auth.model import JWTAdminTokens, JWTTokens
from app.api.auth.schemas import RefreshAdminToken, RefreshToken, TokensPair
from app.api.auth.utils import get_hashed_password, jwt_decode, jwt_encode
from app.api.users.models import Users
from app.api.users.schemas import SUser, SUserWithPassword
from app.config import settings
from app.dao.base import BaseDAO
from app.exceptions import InvalidPasswordOrLoginException, TokenIsInvalidException


class AuthDAO(BaseDAO):

    @classmethod
    async def auth(cls, email_password, is_admin = False) -> TokensPair:

        if is_admin:
            user = await cls.get_admin_by_email(email_password.email)
        else:
            user = await cls.get_user_by_email(email_password.email)
        
        if not user or not cls.check_password(user, email_password.password):
            raise InvalidPasswordOrLoginException

        refresh_token = await cls.get_refresh_token(user, is_admin=is_admin)
        access_token = await cls.get_access_token(refresh_token)

        return TokensPair(refresh_token=refresh_token, access_token=access_token)

    @classmethod
    def check_password(cls, user: SUserWithPassword, password: str) -> bool:

        hash = get_hashed_password(password)
        from_db = user.hashed_password

        return hash == from_db

    @classmethod
    async def get_refresh_token(cls, user: SUserWithPassword | SAdminWithPassword, is_admin = False):
        jti = uuid.uuid4()

        if is_admin:
            sub = user.admin_id
            role = 'admin'
            refresh_token = await AuthDAO.reg_refresh_admin_token(RefreshAdminToken(jti=jti, admin_id=sub))
        else:
            sub = user.user_id
            role = 'user'
            refresh_token = await AuthDAO.reg_refresh_token(RefreshToken(jti=jti, user_id=sub))
        
        exp = datetime.now(tz=timezone.utc) + timedelta(seconds=settings.REFRESH_TOKEN_AGE)

        token_str = jwt_encode({
            'type': 'refresh',
            'sub': sub,
            'role': role,
            'exp': exp,
            'jti': str(refresh_token.jti)
            })
        
        return token_str

    @classmethod
    async def get_access_token(cls, refresh_token: str):
        payload = await cls.check_refresh_token(refresh_token)
        exp = datetime.now(tz=timezone.utc) + timedelta(seconds=settings.REFRESH_TOKEN_AGE)

        return jwt_encode({
            'type': 'access',
            'sub': payload['sub'],
            'role': payload['role'],
            'exp': exp
        })
    
    @classmethod
    async def check_refresh_token(cls, refresh_token: str) -> dict:
        payload = jwt_decode(refresh_token)

        if payload['type'] != 'refresh':
            raise TokenIsInvalidException
        
        if payload['role'] == 'admin':
             if not await cls.select_one_or_none(jti=uuid.UUID(payload['jti']), is_admin=True):
                raise TokenIsInvalidException
        else:
            if not await cls.select_one_or_none(jti=uuid.UUID(payload['jti']), is_admin=False):
                raise TokenIsInvalidException
        return payload
    
    @classmethod
    async def check_access_token(cls, access_token: str) -> dict:
        payload = jwt_decode(access_token)
        return payload
    
    @classmethod
    async def reg_refresh_token(cls, refresh_token: RefreshToken) -> RefreshToken:
        token = await cls.insert(token=refresh_token.model_dump())
        return token

    @classmethod
    async def reg_refresh_admin_token(cls, refresh_token: RefreshAdminToken) -> RefreshAdminToken:
        token = await cls.insert(is_admin=True, token=refresh_token.model_dump())
        return token

    @classmethod
    async def insert(cls, token, is_admin=False):
        if is_admin:
            query = insert(JWTAdminTokens).values(**token).returning(JWTAdminTokens)
        else:
            query = insert(JWTTokens).values(**token).returning(JWTTokens)
        result = await cls._update_base(query)
        return result.scalar_one()

    @classmethod
    async def select_one_or_none(cls, jti: uuid.UUID, is_admin=False):
        if is_admin:
            query = select(JWTAdminTokens.__table__.columns).filter_by(jti=jti)
        else:
            query = select(JWTTokens.__table__.columns).filter_by(jti=jti)
        result = await cls._select(query)
        return result.mappings().one_or_none()

    @classmethod
    async def delete(cls, uid: int, is_admin=False) -> bool:
        if is_admin:
            query = delete(JWTAdminTokens).where(JWTAdminTokens.admin_id == uid)
        else:
            query = delete(JWTTokens).where(JWTTokens.user_id == uid)
        result = await cls._update_base(query)
        return bool(result.rowcount)

    @classmethod
    async def get_user_by_email(cls, email: str) -> SUserWithPassword:
        query = select(Users.__table__.columns).filter_by(email=email)
        result = await cls._select(query)
        return result.mappings().one_or_none()
    
    @classmethod
    async def get_admin_by_email(cls, email: str) -> SAdminWithPassword:
        query = select(Admins.__table__.columns).filter_by(email=email)
        result = await cls._select(query)
        return result.mappings().one_or_none()
