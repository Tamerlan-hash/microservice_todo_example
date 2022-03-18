from fastapi import Depends, status, HTTPException

from app.api.v1.validators import http_exception
from app.api.v1.dals.organization_role_permission_dal import OrganizationRolePermissionDAL
from app.api.v1.dals.organization_dal import OrganizationDAL
from app.api.v1.dals.dependencies import (
    get_organization_role_permission_dal,
    get_organization_dal,
)

from app.helper_functions.jwt import get_account

from app.settings.database_configs.database_connection import async_session


async def create_role_and_permissions():
    async with async_session() as session:
        async with session.begin():
            organization_role_permission_dal = OrganizationRolePermissionDAL(session)
            permissions = [
                "add_account_to_organization",
                "delete_account_from_organization",
                "add_account_to_project",
                "delete_account_from_project",
                "add_account_to_task",
                "delete_account_from_task",
                "create_organization_role",
                "add_permission_to_organization_role",
                "delete_permission_from_organization_role",
                "create_project_for_organization",
                "create_task_for_project",
                "show_organization_project",
                "show_project_tasks",
            ]
            await organization_role_permission_dal.create_role_and_permissions(
                "organization_admin",
                permissions,
            )


def check_organization_permission(request_permissions=[]):
    async def async_check_organization_permission(
        organization_id: int,
        account_id: int = Depends(get_account),
        organization_dal: OrganizationDAL = Depends(get_organization_dal),
        organization_role_permission_dal: OrganizationRolePermissionDAL = Depends(get_organization_role_permission_dal),
    ):
        organization_member = await organization_dal.get_organization_member(account_id, organization_id)
        print("MEMBERRRRRRRR", organization_member)
        member_permissions = await organization_role_permission_dal.get_member_permissions(organization_member.id)
        print("PERMISSIONSSSSSSSSS", member_permissions)
        if len(request_permissions) > 1:
            for request_permission in request_permissions:
                if not request_permission in member_permissions:
                    raise http_exception.PermissionDeniedError
        else:
            request_permission = request_permissions[0]
            if not request_permission in member_permissions:
                raise http_exception.PermissionDeniedError
    return async_check_organization_permission
