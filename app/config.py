from typing import Literal
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST', 'PROD']

    # Для PROD
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Для TEST
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    # Для DEV
    DEV_DB_HOST: str
    DEV_DB_PORT: int
    DEV_DB_USER: str
    DEV_DB_PASS: str
    DEV_DB_NAME: str

    # Для JWT
    JWT_ALGORITHM: str
    JWT_PRIVATE_KEY_PATH: str
    JWT_PUBLIC_KEY_PATH: str

    LONG_TOKEN_AGE_DAYS: int

    PASSWORD_SALT: str

    class Config:
        env_file = '.env'

settings = Settings()
