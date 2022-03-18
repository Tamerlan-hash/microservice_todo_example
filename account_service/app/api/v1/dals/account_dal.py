from app.settings.database_configs.database_connection import async_session as session

from sqlalchemy import or_
from sqlalchemy.future import select
from sqlalchemy import exists

from app.account.models import Account


class AccountDAL:
    def __init__(self, db_session: session):
        self.db_session = db_session

    async def get_account_by_id(self, account_id):
        q = await self.db_session.execute(
            select(Account)
            .filter(Account.id == account_id)
        )
        return q.scalars().first()

    async def check_account_exist_by_id(self, account_id):
        q = await self.db_session.execute(
            exists(
                select(Account.id)
                .filter(Account.id == account_id)
            ).select()
        )
        return q.scalars().first()

    async def create_new_account(self, request, hashed_password):
        new_account = Account(
            username=request.username,
            fullname=request.fullname,
            email=request.email,
            birth_date=request.birth_date,
            hashed_password=hashed_password,
            is_active=True,
        )
        self.db_session.add(new_account)
        await self.db_session.flush()
        return new_account

    async def get_account_by_login(self, login):
        q = await self.db_session.execute(
            select(Account)
            .filter(
                or_(
                    Account.email == login,
                    Account.username == login,
                )
            )
        )
        return q.scalars().first()
