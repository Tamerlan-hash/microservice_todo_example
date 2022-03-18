import datetime

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class AccountSignup(BaseModel):
    username: str
    fullname: str | None
    password: str
    email: EmailStr
    birth_date: datetime.datetime

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class AccountLogin(BaseModel):
    login: str
    password: str

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class AccountPrivateInfoOut(BaseModel):
    id: int
    username: str
    fullname: str | None
    email: EmailStr
    birth_date: datetime.datetime | None

    class Config:
        orm_mode = True
        validate_assignment = True
