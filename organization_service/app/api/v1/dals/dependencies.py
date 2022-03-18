from app.settings.database_configs.database_connection import async_session

from app.api.v1.dals.organization_role_permission_dal import OrganizationRolePermissionDAL
from app.api.v1.dals.organization_dal import OrganizationDAL
from app.api.v1.dals.account_dal import AccountDAL
from app.api.v1.dals.project_dal import ProjectDAL
from app.api.v1.dals.task_dal import TaskDAL


async def get_task_dal():
    async with async_session() as session:
        async with session.begin():
            yield TaskDAL(session)


async def get_project_dal():
    async with async_session() as session:
        async with session.begin():
            yield ProjectDAL(session)


async def get_account_dal():
    async with async_session() as session:
        async with session.begin():
            yield AccountDAL(session)


async def get_organization_role_permission_dal():
    async with async_session() as session:
        async with session.begin():
            yield OrganizationRolePermissionDAL(session)


async def get_organization_dal():
    async with async_session() as session:
        async with session.begin():
            yield OrganizationDAL(session)