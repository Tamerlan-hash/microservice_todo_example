from pydantic import BaseModel, constr


class CreateOrganization(BaseModel):
    organization_name: constr(
        regex=r"^[a-z\d._-]+$"
    )
    title: str
    description: str | None
    is_private: bool

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True


class OrganizationInfoOut(BaseModel):
    id: int
    organization_name: str
    title: str
    description: str
    is_private: bool

    class Config:
        orm_mode = True


class OrganizationMemberInfoOut(BaseModel):
    id: int
    organization_id: int
    account_id: int
    organization_role_id: int

    class Config:
        orm_mode = True


class AddNewMemberToOrganization(BaseModel):
    account_id: int
    role_name: str

    class Config:
        orm_mode = True
        anystr_strip_whitespace = True