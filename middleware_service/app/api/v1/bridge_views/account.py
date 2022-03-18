from fastapi import APIRouter, HTTPException, status, Depends

from app.api.v1.schemas import account_schema

from app.settings import middleware_url

from app.helper_functions.http_request import send_request


account_bridge_router = APIRouter(tags=["Account"])


@account_bridge_router.get(
    "/middleware/check_account",
    status_code=200,
)
async def check_account(account_id: int):
    return await send_request(
        url=f"{middleware_url.ACCOUNT_URL_CHECK_ACCOUNT}",
        method="get",
        params={"account_id": account_id},
    )


@account_bridge_router.post(
    "/middleware/account/create_or_update",
    status_code=200,
)
async def create_or_update_account(
    authorization: str,
    request: account_schema.CreateOrUpdateAccount,
):
    print("1111111111111111111111111111111111")
    print(middleware_url.ORGANIZATION_URL_CREATE_OR_UPDATE_ACCOUNT)
    await send_request(
        url=f"{middleware_url.ORGANIZATION_URL_CREATE_OR_UPDATE_ACCOUNT}",
        method="post",
        params={
            "authorization": authorization
        },
        data=request.dict()
    )
