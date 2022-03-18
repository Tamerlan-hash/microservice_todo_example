from pydantic import BaseModel


class Account(BaseModel):
    account_id: int
    username: str
    fullname: str | None
    avatar: str | None

    class Config:
        orm_mode = True


class AccountId(BaseModel):
    account_id: int

    class Config:
        orm_mode = True
