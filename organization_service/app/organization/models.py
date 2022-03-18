from app.settings.database_configs.base import Base

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, BigInteger, String,
    DateTime, Text, Boolean,
    Integer, Enum, ForeignKey,
    Table,
)

organization_role_permission_association = Table(
    'organization-role-permissions',
    Base.metadata,
    Column('OrganizationRole_id', BigInteger, ForeignKey('OrganizationRoles.id')),
    Column('OrganizationPermission_id', BigInteger, ForeignKey('OrganizationPermissions.id')),
)


class OrganizationPermission(Base):
    __tablename__ = "OrganizationPermissions"
    id = Column(Integer, primary_key=True, index=True)
    permission_name = Column(String(100), nullable=False, unique=True)


class OrganizationRole(Base):
    __tablename__ = 'OrganizationRoles'
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(100), nullable=False, unique=True)
    permissions = relationship(
        "OrganizationPermission",
        secondary=organization_role_permission_association,
        backref='organization_roles',
        lazy='select',
    )


class OrganizationMember(Base):
    __tablename__ = "OrganizationMembers"
    id = Column(BigInteger, primary_key=True, index=True)
    organization_id = Column(BigInteger, ForeignKey("Organizations.id", ondelete="CASCADE"))
    account_id = Column(BigInteger)
    organization_role_id = Column(BigInteger, nullable=True)


class Organization(Base):
    __tablename__ = "Organizations"
    id = Column(BigInteger, primary_key=True, index=True)
    organization_name = Column(String(100), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    avatar = Column(String(500), nullable=True)
    is_private = Column(Boolean, nullable=False)