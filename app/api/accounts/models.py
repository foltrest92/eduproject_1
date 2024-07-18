from app.database import Base

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Accounts(Base):
    __tablename__ = 'accounts'

    account_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True, nullable=False)
    balance = Column(Integer, nullable=False, default=0)

    transactions = relationship('Transactions')