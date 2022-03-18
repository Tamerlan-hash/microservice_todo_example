from fastapi import APIRouter, HTTPException, status, Depends

from app.api.v1.middleware.schemas import account_schema
from app.api.v1.dals.dependencies import get_account_dal
from app.api.v1.dals.account_dal import AccountDAL

from app.helper_functions.jwt import get_account

middleware_account_router = APIRouter(tags=["Middleware"])


@middleware_account_router.post(
    "/middleware/account/create_or_update",
    status_code=201,
)
async def create_or_update_account(
    request: account_schema.CreateOrUpdateAccount,
    account_id: int = Depends(get_account),
    account_dal: AccountDAL = Depends(get_account_dal),
):
    if account_id == request.account_id:
        print("2222222222222222222222")
        result = await account_dal.create_or_update_account(request, account_id)
    else:
        result = None
    print("0000000000000000000000000", result)
