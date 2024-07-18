from uuid import UUID
from pydantic import BaseModel, EmailStr


class TokensPair(BaseModel):
    refresh_token: str
    access_token: str

class RefreshToken(BaseModel):
    jti: UUID
    user_id: int
    revoked: bool = False

class RefreshAdminToken(BaseModel):
    jti: UUID
    admin_id: int
    revoked: bool = False

class EmailPassword(BaseModel):
    email: EmailStr
    password: str