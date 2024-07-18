import hashlib

import jwt
from app.config import settings

def get_hashed_password(password: str) -> str:
    return hashlib.sha256(f'{password}{settings.PASSWORD_SALT}'.encode()).hexdigest()

def jwt_encode(payload:dict):
    return jwt.encode(
        payload=payload,
        algorithm=settings.JWT_ALGORITHM,
        key=settings.JWT_PRIVATE_KEY)

def jwt_decode(encoded: str):
    return jwt.decode(
        jwt=encoded,
        algorithms=settings.JWT_ALGORITHM,
        key=settings.JWT_PUBLIC_KEY)
