from sqlalchemy import UUID, Column, Integer, ForeignKey, Boolean
from app.database import Base


class JWTTokens(Base):
    __tablename__ = 'jwttoken'

    jti = Column(UUID, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    revoked = Column(Boolean, default=False)

class JWTAdminTokens(Base):
    __tablename__ = 'jwtadmintoken'

    jti = Column(UUID, primary_key=True, nullable=False)
    admin_id = Column(Integer, ForeignKey('admins.admin_id'), nullable=False)
    revoked = Column(Boolean, default=False)
