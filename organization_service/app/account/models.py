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
    account_id = Column(BigInteger, unique=True)
    fullname = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    avatar = Column(String(500), nullable=True)
