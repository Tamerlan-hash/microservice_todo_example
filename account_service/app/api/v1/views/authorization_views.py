from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends

from app.api.v1.schemas import account_schema
from app.api.v1.dals.account_dal import AccountDAL
from app.api.v1.dals.dependencies import get_account_dal

from app.helper_functions.cryptography import (
    authenticate_account, create_access_token,
)
from app.settings.config import ACCESS_TOKEN_EXPIRE_MINUTES


authorization_router = APIRouter(tags=["Authorization"])


@authorization_router.post(
    "/accounts/token",
    response_model=account_schema.Token,
    status_code=200,
)
async def create_token(
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

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data_to_encode={"account_id": account.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
