from fastapi import APIRouter, HTTPException, status, Depends

from app.api.v1.schemas import task_schema, account_schema

from app.api.v1.dals.task_dal import TaskDAL
from app.api.v1.dals.dependencies import get_task_dal

from app.helper_functions.jwt import get_account
from app.helper_functions.pagination import CustomPage as Page, paginate

from app.api.v1.validators.project_validator import validate_member_in_project

task_router = APIRouter(tags=["Task"])


@task_router.post(
    "/organizations/projects/tasks",
    status_code=201,
    response_model=task_schema.TaskInfoOut,
    dependencies=[Depends(validate_member_in_project)]
)
async def create_new_task(
    project_id: int,
    request: task_schema.CreateTask,
    task_dal: TaskDAL = Depends(get_task_dal),
):
    new_task = await task_dal.create_new_task(request, project_id)
    return new_task


@task_router.get(
    "/organizations/projects/tasks",
    status_code=200,
    response_model=Page[task_schema.TaskInfoOutAccounts],
    dependencies=[Depends(validate_member_in_project)]
)
async def show_project_tasks(
    project_id: int,
    task_dal: TaskDAL = Depends(get_task_dal),
):
    tasks = await task_dal.get_project_tasks(project_id)
    return await paginate(task_dal.db_session, tasks)


@task_router.get(
    "/organizations/projects/tasks/{task_id}",
    status_code=200,
    response_model=task_schema.TaskInfoOutAccounts,
    dependencies=[Depends(validate_member_in_project)]
)
async def show_project_tasks(
    task_id: int,
    task_dal: TaskDAL = Depends(get_task_dal),
):
    task = await task_dal.get_task(task_id)
    return task



@task_router.post(
    "/organizations/projects/tasks/{task_id}/pin_account",
    status_code=201,
    response_model=task_schema.TaskInfoOutAccounts,
    dependencies=[Depends(validate_member_in_project)]
)
async def pin_account_to_task(
    task_id: int,
    request: account_schema.AccountId,
    task_dal: TaskDAL = Depends(get_task_dal),
):
    await task_dal.pin_account_to_task(task_id, request.account_id)
    return await task_dal.get_task(task_id)


@task_router.post(
    "/organizations/projects/tasks/{task_id}/unpin_account",
    status_code=201,
    response_model=task_schema.TaskInfoOutAccounts,
    dependencies=[Depends(validate_member_in_project)]
)
async def attach_account_to_task(
    task_id: int,
    request: account_schema.AccountId,
    task_dal: TaskDAL = Depends(get_task_dal),
):
    await task_dal.unpin_account_to_task(task_id, request.account_id)
    return await task_dal.get_task(task_id)
