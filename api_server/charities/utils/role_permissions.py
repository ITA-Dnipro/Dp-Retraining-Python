from fastapi import status

from charities.utils.exceptions import CharityEmployeeRolePermissionError
from common.exceptions.charities import CharityExceptionMsgs


def employee_role_validator(employee_roles: list, allowed_roles: list) -> bool:
    """Checks if employee_roles present in list allowed_roles.

    Args:
        employee_roles: A list of employee's role names.
        usernames: A list of allowed role names.

    Raises:
        CharityEmployeeRolePermissionError in case of any role from employee_roles not present in allowed_roles list.

    Returns:
    bool of comparison of two values.
    """
    check = any(employee_role in allowed_roles for employee_role in employee_roles)
    if check:
        return check
    raise CharityEmployeeRolePermissionError(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=CharityExceptionMsgs.NO_CHARITY_EMPLOYEE_ROLE_PERMISSION.value.format(
            employee_roles=employee_roles,
        ),
    )
