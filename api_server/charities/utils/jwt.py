from fastapi import status

from charities.utils.exceptions import CharityEmployeePermissionError
from common.exceptions.charities import CharityExceptionMsgs


def jwt_charity_validator(jwt_subject: str, usernames: list) -> bool:
    """Checks if jwt_identity present in list charity employees.

    Args:
        jwt_subject: Value decoded from jwt source.
        usernames: A list with User's usernames.

    Raises:
        CharityEmployeePermissionError in case of employee.user.username not present
        in charity employee's usernames list.

    Returns:
    bool of comparison of two values.
    """
    check = jwt_subject in usernames
    if check:
        return check
    raise CharityEmployeePermissionError(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=CharityExceptionMsgs.NO_CHARITY_EMPLOYEE_PERMISSION.value,
    )
