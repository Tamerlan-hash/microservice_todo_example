from pydantic import BaseModel


class CreateOrUpdateAccount(BaseModel):
    account_id: int
    username: str
    fullname: str | None
