from fastapi import status

from common.exceptions.users import UserExceptionMsgs
from users.utils.exceptions import UserPermissionError


def jwt_user_validator(jwt_subject: str, username: str) -> bool:
    """Checks equality of two values jwt_identity and user's username.

    Args:
        jwt_subject: Value decoded from jwt source.
        username: User's username.

    Raises:
        UserPermissionError.

    Returns:
    bool of comparison of two values.
    """
    check = jwt_subject == username
    if check:
        return check
    raise UserPermissionError(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=UserExceptionMsgs.NO_USER_PERMISSIONS.value,
    )
