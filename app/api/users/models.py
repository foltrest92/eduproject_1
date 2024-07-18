from app.database import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    accounts = relationship("Accounts")
    transactions = relationship('Transactions')
