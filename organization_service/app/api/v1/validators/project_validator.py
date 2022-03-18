from fastapi import Depends

from app.api.v1.schemas import project_schema

from app.api.v1.dals.dependencies import get_project_dal
from app.api.v1.dals.project_dal import ProjectDAL

from app.api.v1.validators import http_exception

from app.helper_functions.jwt import get_account


async def check_project_name(
    request: project_schema.CreateProject,
    project_dal: ProjectDAL = Depends(get_project_dal),
) -> None:
    is_exist = await project_dal.check_project_name(request.project_name.lower())
    if is_exist:
        raise http_exception.ProjectAlreadyExistError


async def validate_member_in_project(
    project_id: int,
    account_id: int = Depends(get_account),
    project_dal: ProjectDAL = Depends(get_project_dal),
) -> None:
    is_member = await project_dal.check_project_member(
        account_id, project_id,
    )
    if not is_member:
        raise http_exception.ProjectDoesNotExistError
