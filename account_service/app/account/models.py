from sqlalchemy.sql import func
from sqlalchemy import (
    Column, BigInteger, String,
    DateTime, Text, Boolean,
    Integer, Enum, ForeignKey
)

from app.settings.database_configs.base import Base


class Account(Base):
    __tablename__ = "Accounts"
    id = Column(BigInteger, primary_key=True, index=True)
    fullname = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    birth_date = Column(DateTime, nullable=False)
    avatar = Column(String(500), nullable=True)
    hashed_password = Column(Text, nullable=True)
    joined = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=False)
    role_id = Column(Integer, nullable=True)
