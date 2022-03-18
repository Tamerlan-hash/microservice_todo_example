from app.settings.database_configs.database_connection import async_session

from app.api.v1.dals.account_dal import AccountDAL


async def get_account_dal():
    async with async_session() as session:
        async with session.begin():
            yield AccountDAL(session)