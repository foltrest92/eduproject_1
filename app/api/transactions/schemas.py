from uuid import UUID
from pydantic import BaseModel

class STransactionBase(BaseModel):
    transaction_id: UUID
    user_id: int
    account_id: int
    amount: int

class STransaction(STransactionBase):
    signature: str

