from sqlalchemy import Column, Integer
from app.database import Base


class Account(Base):
    __tablename__ = 'accounts'

    account_id = Column(Integer, primary_key=True, nullable=False)