from fastapi import APIRouter, HTTPException, status, Depends

from app.api.v1.dals.account_dal import AccountDAL
from app.api.v1.dals.dependencies import get_account_dal

middleware_account_router = APIRouter(tags=["Middleware"])


@middleware_account_router.get(
    "/middleware/check_account",
    status_code=200,
)
async def check_account(
    account_id: int,
    account_dal: AccountDAL = Depends(get_account_dal)
):
    account_exist = await account_dal.check_account_exist_by_id(account_id)
    print("EXISTS", account_exist)
    return account_exist
