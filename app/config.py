from typing import Literal
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    def __init__(self) -> None:
        super().__init__(self)
        with open(self.JWT_PRIVATE_KEY_PATH) as f:
            self.JWT_PRIVATE_KEY = f.read()
        with open(self.JWT_PUBLIC_KEY_PATH) as f:
            self.JWT_PUBLIC_KEY = f.read()

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

    REFRESH_TOKEN_AGE: int
    ACCESS_TOKEN_AGE: int

    PASSWORD_SALT: str

    PAYMENTS_SECRET_KEY: str

    JWT_PRIVATE_KEY: str | None = None
    JWT_PUBLIC_KEY: str | None = None

    class Config:
        env_file = '.env'
    

settings = Settings()
