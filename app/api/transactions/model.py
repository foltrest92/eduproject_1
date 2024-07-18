from app.database import Base
from sqlalchemy import UUID, Column, Integer, ForeignKey

class Transactions(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(UUID, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.account_id'), nullable=False)
    amount = Column(Integer, nullable=False)
