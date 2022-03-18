from fastapi import APIRouter, HTTPException, status, Depends

from app.api.v1.schemas import project_schema, account_schema

from app.api.v1.dals.project_dal import ProjectDAL
from app.api.v1.dals.dependencies import get_project_dal

from app.helper_functions.jwt import get_account
from app.helper_functions.pagination import CustomPage as Page, paginate

from app.helper_functions.check_organization_permission import check_organization_permission

from app.api.v1.validators.organization_validator import (
    validate_is_member_of_organization,
)
from app.api.v1.validators.project_validator import (
    check_project_name,
    validate_member_in_project,
)


project_router = APIRouter(tags=["Project"])


@project_router.post(
    "/organizations/projects",
    status_code=201,
    response_model=project_schema.ProjectInfoOut,
    dependencies=[
        Depends(validate_is_member_of_organization),
        Depends(check_organization_permission(
            request_permissions=["create_project_for_organization"]
        )),
        Depends(check_project_name)
    ]
)
async def create_new_project(
    organization_id: int,
    request: project_schema.CreateProject,
    account_id: int = Depends(get_account),
    project_dal: ProjectDAL = Depends(get_project_dal),
):
    new_project = await project_dal.create_project(request, account_id, organization_id)
    return new_project


@project_router.get(
    "/organizations/projects",
    status_code=200,
    response_model=Page[project_schema.ProjectInfoOut],
    dependencies=[
        Depends(validate_is_member_of_organization),
        Depends(check_organization_permission(
            request_permissions=["show_organization_project"]
        )),
    ]
)
async def show_organization_projects(
    organization_id: int,
    account_id: int = Depends(get_account),
    project_dal: ProjectDAL = Depends(get_project_dal),
):
    projects = await project_dal.show_organization_projects(account_id, organization_id)
    return await paginate(project_dal.db_session, projects)


@project_router.get(
    "/organizations/projects/{project_id:int}",
    status_code=200,
    response_model=project_schema.ProjectInfoOut,
    dependencies=[
        Depends(validate_is_member_of_organization),
        Depends(validate_member_in_project),
        Depends(check_organization_permission(
            request_permissions=[
                "show_organization_project",
                "show_project_tasks",
            ]
        )),
    ]
)
async def show_project(
    project_id: int,
    project_dal: ProjectDAL = Depends(get_project_dal),
):
    project = await project_dal.get_project(project_id)
    return project


@project_router.post(
    "/organizations/projects/{project_id}/members",
    status_code=201,
    response_model=Page[project_schema.ProjectMemberInfoOut],
    dependencies=[
        Depends(validate_is_member_of_organization),
        Depends(check_organization_permission(
            request_permissions=["add_account_to_project"]
        )),
    ]
)
async def add_member_to_project(
    project_id: int,
    request: account_schema.AccountId,
    project_dal: ProjectDAL = Depends(get_project_dal),
):
    await project_dal.create_project_member(
        request.account_id, project_id
    )
    members = await project_dal.get_project_members(project_id)
    return await paginate(project_dal.db_session, members)


@project_router.get(
    "/organizations/projects/{project_id}/members",
    status_code=201,
    response_model=Page[project_schema.ProjectMemberInfoOut],
    dependencies=[
        Depends(validate_member_in_project),
        Depends(validate_is_member_of_organization),
        Depends(check_organization_permission(
            request_permissions=["show_organization_project"]
        )),
    ]
)
async def show_project_members(
    project_id: int,
    project_dal: ProjectDAL = Depends(get_project_dal),
):
    members = await project_dal.get_project_members(project_id)
    return await paginate(project_dal.db_session, members)
