from app.settings.database_configs.database_connection import async_session as session

from sqlalchemy import exists, insert
from sqlalchemy.future import select

from app.organization.models import (
    Organization, OrganizationMember,
)
from app.api.v1.dals.organization_role_permission_dal import OrganizationRolePermissionDAL


class OrganizationDAL:
    def __init__(self, db_session: session):
        self.db_session = db_session

    async def get_organization_member_associations(self, account_id):
        q = await self.db_session.execute(
            select(OrganizationMember.organization_id)
            .filter(
                OrganizationMember.account_id == account_id,
            )
        )
        return q.scalars().all()

    async def get_organizations(self, account_id):
        organization_member_associations = await self.get_organization_member_associations(account_id)
        q = (
            select(Organization)
            .filter(Organization.id.in_(organization_member_associations))
        )
        return q

    async def check_organization_is_private(self, organization_id):
        q = await self.db_session.execute(
            select(Organization.is_private)
            .filter(Organization.id == organization_id)
        )
        return q.scalars().first()

    async def check_organization_member(self, account_id, organization_id):
        q = await self.db_session.execute(
            exists(
                select(OrganizationMember)
                .filter(
                    OrganizationMember.organization_id == organization_id,
                    OrganizationMember.account_id == account_id,
                )
            ).select()
        )
        return q.scalars().first()

    async def get_organization(self, organization_id):
        q = await self.db_session.execute(
            select(Organization)
            .filter(Organization.id == organization_id)
        )

        return q.scalars().first()

    async def get_organization_member(self, account_id, organization_id):
        q = await self.db_session.execute(
            select(OrganizationMember)
            .filter(
                OrganizationMember.organization_id == organization_id,
                OrganizationMember.account_id == account_id
            )
        )
        return q.scalars().first()

    async def create_organization_member(self, account_id, organization_id, role_name):
        is_organization_member = await self.check_organization_member(account_id, organization_id)
        if not is_organization_member:
            organization_role_id = (
                await OrganizationRolePermissionDAL(self.db_session).get_organization_role_id_by_role_name(role_name)
            )
            if not organization_role_id:
                organization_role = (
                    await OrganizationRolePermissionDAL(self.db_session).create_new_organization_role(role_name)
                )
                organization_role_id = organization_role.id
            organization_member = OrganizationMember(
                organization_id=organization_id,
                account_id=account_id,
                organization_role_id=organization_role_id,
            )
            self.db_session.add(organization_member)
            await self.db_session.flush()
            return organization_member
        else:
            return await self.get_organization_member(account_id, organization_id)

    async def create_organization(self, request, account_id):
        new_organization = Organization(
            organization_name=request.organization_name.lower(),
            title=request.title,
            description=request.description,
            is_private=request.is_private,
        )
        self.db_session.add(new_organization)
        await self.db_session.flush()

        await self.create_organization_member(
            account_id, new_organization.id, "organization_admin")

        return new_organization

    async def check_organization_name(self, organization_name):
        q = await self.db_session.execute(
            exists(
                select(Organization)
                .filter(Organization.organization_name == organization_name)
            ).select()
        )
        return q.scalars().first()

    async def get_organization_members(self, organization_id):
        q = (
            select(OrganizationMember)
            .filter(OrganizationMember.organization_id == organization_id)
        )
        return q
