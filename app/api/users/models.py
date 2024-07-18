import uuid
from app.database import Base
from sqlalchemy import Column, Integer, String, UUID

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    