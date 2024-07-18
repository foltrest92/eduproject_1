from pydantic import BaseModel

class SUserBase(BaseModel):
    email: str
    full_name: str

class SNewUser(SUserBase):
    password: str

class SUpdateUser(BaseModel):
    email: str | None = None
    full_name: str | None = None
    password: str | None = None

class SUser(SUserBase):
    user_id: int

class SUserWithPassword(SUser):
    hashed_password: str