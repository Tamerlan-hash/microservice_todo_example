from datetime import timedelta

from app.helper_functions.cryptography import (
    get_password_hash, create_access_token, authenticate_account,
)
from app.helper_functions.http_request import send_request

from app.api.v1.schemas import account_schema

from app.api.v1.dals.account_dal import AccountDAL
from app.api.v1.dals.dependencies import get_account_dal

from fastapi import APIRouter, HTTPException, status, Depends

from app.settings import middleware_url

registration_router = APIRouter(tags=["Registration"])


@registration_router.post(
    "/accounts",
    response_model=account_schema.AccountPrivateInfoOut,
    status_code=201,
)
async def create_account(
    request: account_schema.AccountSignup,
    account_dal: AccountDAL = Depends(get_account_dal)
):
    hashed_password = get_password_hash(request.password)
    new_account = await account_dal.create_new_account(request, hashed_password)
    return new_account


@registration_router.post(
    "/accounts/create_or_update",
    response_model=account_schema.AccountPrivateInfoOut,
    status_code=201,
)
async def create_or_update_account(
    request: account_schema.AccountLogin,
    account_dal: AccountDAL = Depends(get_account_dal)
):
    account = await authenticate_account(request.login, request.password, account_dal)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "IncorrectLoginOrPasswordError"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_account = await account_dal.get_account_by_login(request.login)
    access_token_expires = timedelta(minutes=1)
    access_token = create_access_token(
        data_to_encode={"account_id": new_account.id}, expires_delta=access_token_expires
    )
    await send_request(
        url=f"{middleware_url.MIDDLEWARE_URL_CREATE_OR_UPDATE_ACCOUNT}",
        method="post",
        data={
            "account_id": new_account.id,
            "fullname": new_account.fullname,
            "username": new_account.username,
        },
        params={
            "authorization": "bearer " + access_token
        }
    )
    return new_account