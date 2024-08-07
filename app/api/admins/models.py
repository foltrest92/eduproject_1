from app.database import Base
from sqlalchemy import Column, Integer, String

class Admins(Base):
    __tablename__ = 'admins'

    admin_id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    