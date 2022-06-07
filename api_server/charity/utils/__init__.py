from sqlalchemy.ext.associationproxy import _AssociationList
from starlette.status import HTTP_400_BAD_REQUEST

from charity.utils.exceptions import OrganisationHTTPException


def check_permission_to_manage_charity(users: _AssociationList, current_user_id: str) -> bool:
    """
    Checks if current User is able to manage organisation.

        Args:
            users: _AssociationList of users
            current_user_id: id of current authenticated User
        Returns:
            True if user's id found in users that can manage charity organisation, neither False.
    """
    for user in users:
        if str(user.id) == current_user_id:
            return True
    return False


def remove_nullable_params(organisation_data: dict) -> dict:
    """
        Checks if current User is able to manage organisation.

        Args:
            organisation_data: dict of validated JSON request
        Returns:
            Dictionary of non - nullable parameters or raises NonValidRequestError
    """
    for key in list(organisation_data.keys()):
        if organisation_data[key] is None:
            organisation_data.pop(key)
    if not organisation_data:
        raise OrganisationHTTPException(status_code=HTTP_400_BAD_REQUEST, detail="No valid request has been passed")
    return organisation_data
