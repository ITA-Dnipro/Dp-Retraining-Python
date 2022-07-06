from fastapi import status

from common.exceptions.fundraisers import FundraiseExceptionMsgs
from fundraisers.utils.exceptions import FundraisePermissionError


def jwt_fundraise_validator(jwt_subject: str, usernames: list) -> bool:
    """Checks if jwt_identity present in list charity.employees user usernames.

    Args:
        jwt_subject: Value decoded from jwt source.
        usernames: list of charity employees usernames.

    Raises:
        FundraisePermissionError in case of user's username not present in charity employees usernames list.

    Returns:
    bool of comparison of two values.
    """
    check = jwt_subject in usernames
    if check:
        return check
    raise FundraisePermissionError(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=FundraiseExceptionMsgs.NO_EMPLOYEE_PERMISSIONS.value,
    )
