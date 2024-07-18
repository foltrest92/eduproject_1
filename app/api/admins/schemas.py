from pydantic import BaseModel

class SAdminBase(BaseModel):
    email: str
    full_name: str

class SNewAdmin(SAdminBase):
    password: str

class SUpdateAdmin(BaseModel):
    admin_id: int | None = None
    email: str | None = None
    full_name: str | None = None
    password: str | None = None



class SAdmin(SAdminBase):
    admin_id: int
    
class SAdminWithPassword(SAdmin):
    hashed_password: str