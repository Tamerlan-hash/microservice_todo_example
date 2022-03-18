import jwt

from fastapi import Header, HTTPException, status

from app.settings import config
from app.settings import middleware_url

from app.api.v1.validators import http_exception

from app.helper_functions.http_request import send_request


async def decode(token: str | None):
    print("TOKEN", token)
    if not token:
        return None
    token = token.split()
    if len(token) != 2:
        return None
    if token[0].lower() != "bearer":
        return None
    token = token[1]
    if token is None:
        return None
    try:
        data = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.ALGORITHM],
        )
        print("DATA", data)
        account_id = data.get("account_id")
        if account_id is None:
            return None
    except jwt.PyJWTError:
        return None
    return account_id


async def check_account(account_id: int):
    is_account = await send_request(
        url=f"{middleware_url.MIDDLEWARE_URL_CHECK_ACCOUNT}",
        method="get",
        params={"account_id": account_id},
    )
    print(middleware_url.MIDDLEWARE_URL_CHECK_ACCOUNT)
    print("000000000000000", is_account)
    return is_account


async def get_account(authorization: str | None):
    account_id = await decode(authorization)
    if account_id is None:
        raise http_exception.NoSuchTokenError
    checker = await check_account(account_id)
    if checker != True:
        raise http_exception.NoSuchTokenError
    return account_id

