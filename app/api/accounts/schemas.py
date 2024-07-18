from pydantic import BaseModel

class SAccountBase(BaseModel):
    user_id: int

class SAccount(SAccountBase):
    account_id: int
    user_id: int
    balance: int = 0
