from app.settings.database_configs.database_connection import async_session as session

from sqlalchemy import exists, update
from sqlalchemy.future import select

from app.account.models import Account


class AccountDAL:
    def __init__(self, db_session: session):
        self.db_session = db_session

    async def check_account_exist_by_id(self, account_id):
        q = await self.db_session.execute(
            exists(
                select(Account.id)
                .filter(Account.account_id == account_id)
            ).select()
        )
        return q.scalars().first()

    async def create_or_update_account(self, request, account_id):
        account_exist = await self.check_account_exist_by_id(account_id)
        if not account_exist:
            new_account = Account(
                account_id=request.account_id,
                fullname=request.fullname,
                username=request.username,
            )
            self.db_session.add(new_account)
            await self.db_session.flush()
            return "OK"
        else:
            q = update(Account).filter(Account.account_id == account_id)
            q.values(
                account_id=account_id,
                fullname=request.fullname,
                username=request.username,
            )
            q.execution_options(synchronize_session="fetch")
            await self.db_session.execute(q)
            return "OK"

