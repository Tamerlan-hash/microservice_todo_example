from fastapi import Header, HTTPException, status


NoSuchTokenError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail={"message": "NoSuchTokenError"},
)


PermissionDeniedError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail={"message": "PermissionDeniedError"},
)


AccountDoesNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={"message": "AccountDoesNotExist"},
)


ItsNotYourOrganizationError = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail={"message": "ItsNotYourOrganizationError"},
)
OrganizationDoesNotExistError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={"message": "OrganizationDoesNotExistError"},
)
OrganizationAlreadyExistError = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"message": "OrganizationAlreadyExistError"},
)


ProjectAlreadyExistError = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"message": "OrganizationAlreadyExistError"},
)
ProjectDoesNotExistError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail={"message": "ProjectDoesNotExistError"},
)