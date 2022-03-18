from app.settings.database_configs.database_connection import async_session as session

from app.task.models import Task
from app.task.models import accounts_task_association

from sqlalchemy import exists, insert, delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


class TaskDAL:
    def __init__(self, db_session: session):
        self.db_session = db_session

    async def create_new_task(self, request, project_id):
        new_task = Task(
            title=request.title,
            description=request.description,
            project_id=project_id,
            deadline=request.deadline,
        )
        self.db_session.add(new_task)
        await self.db_session.flush()

        return new_task

    async def get_project_tasks(self, project_id):
        q = (
            select(Task)
            .options(
                selectinload(Task.accounts)
            )
            .filter(Task.project_id == project_id)
        )
        return q

    async def get_task(self, task_id):
        q = await self.db_session.execute(
            select(Task)
            .options(
                selectinload(Task.accounts)
            )
            .filter(Task.id == task_id)
        )
        return q.scalars().first()

    async def check_account_task_attached(self, task_id, account_id):
        q = await self.db_session.execute(
            exists(
                select(accounts_task_association)
                .filter(
                    accounts_task_association.c.Task_id == task_id,
                    accounts_task_association.c.Account_id == account_id
                )
            ).select()
        )
        return q.scalars().first()

    async def pin_account_to_task(self, task_id, account_id):
        account_attached = await self.check_account_task_attached(task_id, account_id)
        if not account_attached:
            await self.db_session.execute(
                insert(accounts_task_association)
                .values(
                    Task_id=task_id,
                    Account_id=account_id
                )
            )

    async def unpin_account_to_task(self, task_id, account_id):
        await self.db_session.execute(
            delete(accounts_task_association)
            .filter(
                accounts_task_association.c.Task_id == task_id,
                accounts_task_association.c.Account_id == account_id,
            )
        )
