from app.settings.database_configs.database_connection import async_session as session

from sqlalchemy import exists, insert
from sqlalchemy.future import select

from app.organization.models import OrganizationPermission, OrganizationRole, OrganizationMember
from app.organization.models import organization_role_permission_association


class OrganizationRolePermissionDAL:
    def __init__(self, db_session: session):
        self.db_session = db_session

    async def get_organization_role_id_by_member_id(self, member_id):
        q = await self.db_session.execute(
            select(OrganizationMember.organization_role_id)
            .filter(OrganizationMember.id == member_id)
        )
        return q.scalars().first()

    async def get_member_permissions(self, member_id):
        organization_role_id = await self.get_organization_role_id_by_member_id(member_id)
        print("11111111111111111111111111111111111", organization_role_id)
        q = await self.db_session.execute(
            select(OrganizationPermission.permission_name)
            .select_from(OrganizationRole)
            .join(OrganizationRole.permissions)
            .filter(
                OrganizationRole.id == organization_role_id
            )
        )
        return q.scalars().all()

    async def create_new_organization_role(self, role_name):
        new_organization_role = OrganizationRole(
            role_name=role_name
        )
        self.db_session.add(new_organization_role)
        await self.db_session.flush()
        return new_organization_role

    async def get_organization_role_id_by_role_name(self, role_name):
        q = await self.db_session.execute(
            select(OrganizationRole.id)
            .filter(OrganizationRole.role_name == role_name)
        )
        return q.scalars().first()

    async def check_permission_exist_by_name(self, permission_name):
        q = await self.db_session.execute(
            exists(
                select(OrganizationPermission)
                .filter(OrganizationPermission.permission_name == permission_name)
            ).select()
        )
        return q.scalars().first()

    async def check_role_exist_by_name(self, role_name):
        q = await self.db_session.execute(
            exists(
                select(OrganizationRole)
                .filter(OrganizationRole.role_name == role_name)
            ).select()
        )
        return q.scalars().first()

    async def create_role_and_permissions(self, role_name: str, permissions=[]):
        role_created = await self.check_role_exist_by_name(role_name)
        if not role_created:
            role = OrganizationRole(
                role_name=role_name,
            )
            self.db_session.add(role)
            await self.db_session.flush()
        else:
            q = await self.db_session.execute(
                select(OrganizationRole)
                .filter(OrganizationRole.role_name == role_name)
            )
            role = q.scalars().first()

        for permission in permissions:
            permission_created = await self.check_permission_exist_by_name(permission)
            if not permission_created:
                new_organization_permission = OrganizationPermission(
                    permission_name=permission
                )
                self.db_session.add(new_organization_permission)
                await self.db_session.flush()

                await self.db_session.execute(
                    insert(organization_role_permission_association)
                    .values(
                        OrganizationRole_id=role.id,
                        OrganizationPermission_id=new_organization_permission.id,
                    )
                )