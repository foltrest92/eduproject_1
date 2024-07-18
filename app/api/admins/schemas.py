from pydantic import BaseModel

class SAdminBase(BaseModel):
    email: str
    full_name: str

class SAdmin(SAdminBase):
    admin_id: int
