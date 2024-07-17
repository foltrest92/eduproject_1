import uuid
from app.database import Base
from sqlalchemy import Column, Integer, String, UUID

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    