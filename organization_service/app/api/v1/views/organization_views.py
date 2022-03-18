from fastapi import APIRouter, HTTPException, status, Depends

from app.api.v1.dals.organization_dal import OrganizationDAL
from app.api.v1.dals.dependencies import get_organization_dal

from app.helper_functions.jwt import get_account
from app.helper_functions.check_organization_permission import check_organization_permission
from app.helper_functions.pagination import CustomPage as Page, paginate

from app.api.v1.schemas import organization_schema

from app.api.v1.validators.organization_validator import (
    validate_is_member_of_organization,
    validate_show_organization,
    check_organization_name,
    check_organization_candidate,
)

organization_router = APIRouter(tags=["Organization"])


@organization_router.post(
    "/organizations",
    status_code=201,
    response_model=organization_schema.OrganizationInfoOut,
    dependencies=[Depends(check_organization_name)]
)
async def create_organization(
    request: organization_schema.CreateOrganization,
    account_id: int = Depends(get_account),
    organization_dal: OrganizationDAL = Depends(get_organization_dal),
):
    new_organization = await organization_dal.create_organization(request, account_id)
    return new_organization


@organization_router.get(
    "/organizations",
    status_code=200,
    response_model=Page[organization_schema.OrganizationInfoOut]
)
async def show_organizations_membership(
    account_id: int = Depends(get_account),
    organization_dal: OrganizationDAL = Depends(get_organization_dal),
):
    organizations = await organization_dal.get_organizations(account_id)
    return await paginate(organization_dal.db_session, organizations)


@organization_router.post(
    "/organizations/{organization_id}/members",
    status_code=201,
    response_model=organization_schema.OrganizationMemberInfoOut,
    dependencies=[
        Depends(validate_is_member_of_organization),
        Depends(check_organization_candidate),
        Depends(check_organization_permission(request_permissions=["add_account_to_organization"])),
    ]
)
async def add_new_members_to_organization(
    organization_id: int,
    request: organization_schema.AddNewMemberToOrganization,
    organization_dal: OrganizationDAL = Depends(get_organization_dal),
):
    new_member = await organization_dal.create_organization_member(
        request.account_id, organization_id, request.role_name)
    return new_member


@organization_router.get(
    "/organizations/{organization_id:int}",
    status_code=201,
    response_model=organization_schema.OrganizationInfoOut,
    dependencies=[Depends(validate_show_organization)]
)
async def show_organization(
    organization_id: int,
    organization_dal: OrganizationDAL = Depends(get_organization_dal),
):
    organization = await organization_dal.get_organization(organization_id)
    return organization


@organization_router.get(
    "/organizations/{organization_id}/members",
    status_code=200,
    response_model=Page[organization_schema.OrganizationMemberInfoOut],
    dependencies=[Depends(validate_show_organization)],
)
async def show_organization_members(
    organization_id: int,
    organization_dal: OrganizationDAL = Depends(get_organization_dal),
):
    organization_members = await organization_dal.get_organization_members(organization_id)
    return await paginate(organization_dal.db_session, organization_members)