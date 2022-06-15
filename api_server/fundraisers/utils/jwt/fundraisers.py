from fastapi import status

from common.exceptions.fundraisers import FundraiseExceptionMsgs
from fundraisers.utils.exceptions import FundraisePermissionError


def jwt_fundraise_validator(jwt_subject: str, usernames: list) -> bool:
    """Checks if jwt_identity present in list charity users.

    Args:
        jwt_subject: Value decoded from jwt source.
        username: User's username.

    Raises:
        FundraisePermissionError in case of user not present in charity users list.

    Returns:
    bool of comparison of two values.
    """
    check = jwt_subject in usernames
    if check:
        return check
    raise FundraisePermissionError(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=FundraiseExceptionMsgs.NO_USER_PERMISSIONS.value,
    )
