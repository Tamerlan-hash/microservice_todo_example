from fastapi import Depends

from app.helper_functions.jwt import get_account, check_account

from app.api.v1.dals.organization_dal import OrganizationDAL
from app.api.v1.dals.dependencies import get_organization_dal

from app.api.v1.validators import http_exception

from app.api.v1.schemas import organization_schema


async def validate_is_member_of_organization(
    organization_id: int,
    account_id: int = Depends(get_account),
    organization_dal: OrganizationDAL = Depends(get_organization_dal),
) -> None:
    is_member = await organization_dal.check_organization_member(
        account_id, organization_id,
    )
    if not is_member:
        raise http_exception.ItsNotYourOrganizationError


async def validate_show_organization(
    organization_id: int,
    account_id: int = Depends(get_account),
    organization_dal: OrganizationDAL = Depends(get_organization_dal),
) -> None:
    is_private = await organization_dal.check_organization_is_private(organization_id)
    if is_private:
        is_member = await organization_dal.check_organization_member(
            account_id, organization_id,
        )
        if not is_member:
            raise http_exception.OrganizationDoesNotExistError


async def check_organization_name(
    request: organization_schema.CreateOrganization,
    organization_dal: OrganizationDAL = Depends(get_organization_dal),
) -> None:
    is_exist = await organization_dal.check_organization_name(request.organization_name.lower())
    if is_exist:
        raise http_exception.OrganizationAlreadyExistError


async def check_organization_candidate(
    request: organization_schema.AddNewMemberToOrganization,
):
    account_exist = await check_account(request.account_id)
    if not account_exist:
        raise http_exception.AccountDoesNotExist