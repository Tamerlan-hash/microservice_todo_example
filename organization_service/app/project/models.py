from app.settings.database_configs.base import Base

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, BigInteger, String,
    DateTime, Text, Boolean,
    Integer, Enum, ForeignKey,
    Table,
)


class Project(Base):
    __tablename__ = "Projects"
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String(100), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    avatar = Column(String(500), nullable=True)
    organization_id = Column(BigInteger, ForeignKey("Organizations.id"))


class ProjectMember(Base):
    __tablename__ = "ProjectMembers"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(BigInteger)
    project_id = Column(BigInteger, ForeignKey("Projects.id", ondelete="CASCADE"))

