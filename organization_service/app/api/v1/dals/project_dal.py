from app.settings.database_configs.database_connection import async_session as session

from app.project.models import Project, ProjectMember

from sqlalchemy.future import select
from sqlalchemy import exists


class ProjectDAL:
    def __init__(self, db_session: session):
        self.db_session = db_session

    async def check_project_name(self, project_name):
        q = await self.db_session.execute(
            exists(
                select(Project.id)
                .filter(Project.project_name == project_name)
            ).select()
        )
        return q.scalars().first()

    async def get_organization_project_member_associations(self, account_id):
        q = await self.db_session.execute(
            select(ProjectMember.project_id)
            .filter(
                ProjectMember.account_id == account_id,
            )
        )
        return q.scalars().all()

    async def show_organization_projects(self, account_id, organization_id):
        project_associations = await self.get_organization_project_member_associations(account_id)
        q = (
            select(Project)
            .filter(
                Project.id.in_(project_associations),
                Project.organization_id == organization_id
            )
        )
        return q

    async def get_project(self, project_id):
        q = await self.db_session.execute(
            select(Project)
            .filter(Project.id == project_id)
        )
        return q.scalars().first()

    async def check_project_member(self, account_id, project_id):
        q = await self.db_session.execute(
            exists(
                select(ProjectMember)
                .filter(
                    ProjectMember.project_id == project_id,
                    ProjectMember.account_id == account_id,
                )
            ).select()
        )
        return q.scalars().first()

    async def get_project_member(self, account_id, project_id):
        q = await self.db_session.execute(
            select(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.account_id == account_id,
            )
        )
        return q.scalars().first()

    async def get_project_members(self, project_id):
        q = (
            select(ProjectMember)
            .filter(ProjectMember.project_id == project_id)
        )
        return q

    async def create_project_member(self, account_id, project_id):
        is_project_member = await self.check_project_member(account_id, project_id)
        if not is_project_member:
            project_member = ProjectMember(
                account_id=account_id,
                project_id=project_id,
            )
            self.db_session.add(project_member)
            await self.db_session.flush()
            return project_member
        else:
            return await self.get_project_member(account_id, project_id)

    async def create_project(self, request, account_id, organization_id):
        new_project = Project(
            project_name=request.project_name,
            title=request.title,
            description=request.description,
            organization_id=organization_id,
        )
        self.db_session.add(new_project)
        await self.db_session.flush()

        await self.create_project_member(
            account_id, new_project.id
        )

        return new_project
