from pydantic import BaseModel, constr


class CreateProject(BaseModel):
    project_name: constr(
        regex=r"^[a-z\d._-]+$"
    )
    title: str
    description: str | None

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class ProjectInfoOut(BaseModel):
    id: int
    project_name: str
    title: str
    description: str | None
    avatar: str | None
    organization_id: int

    class Config:
        orm_mode = True


class ProjectMemberInfoOut(BaseModel):
    id: int
    account_id: int
    project_id: int

    class Config:
        orm_mode = True
