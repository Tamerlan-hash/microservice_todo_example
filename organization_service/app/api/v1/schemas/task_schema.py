import datetime

from pydantic import BaseModel

from app.api.v1.schemas.account_schema import Account


class CreateTask(BaseModel):
    title: str
    description: str | None
    deadline: datetime.datetime | None

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class TaskInfoOut(BaseModel):
    id: int
    title: str
    description: str | None
    project_id: int
    deadline: datetime.datetime | None

    class Config:
        orm_mode = True


class TaskInfoOutAccounts(TaskInfoOut):
    accounts: list[Account] | None

    class Config:
        orm_mode = True
        validate_assignment = True
