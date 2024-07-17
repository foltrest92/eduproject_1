from uuid import UUID
from pydantic import BaseModel


class SUserBase(BaseModel):
    email: str
    full_name: str

class SUser(SUserBase):
    user_id: UUID