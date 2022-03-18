from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.settings import config
from typing import Optional


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    data_to_encode: dict, expires_delta: timedelta | None = None
):
    to_encode = data_to_encode.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_account(login: str, password: str, account_orm):
    account = await account_orm.get_account_by_login(login)
    if not account:
        return False
    if not verify_password(password, account.hashed_password):
        return False
    return account