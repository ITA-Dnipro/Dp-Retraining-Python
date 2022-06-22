from fastapi import status

from charities.utils.exceptions import CharityEmployeeRolePermissionError, EmployeeRoleNotSupportedError
from common.constants.charities import CharityEmployeeAllowedRolesConstants
from common.exceptions.charities import CharityEmployeesExceptionMsgs, EmployeeRolesExceptionMsgs


def employee_role_validator(employee_roles: list, allowed_roles: tuple) -> bool:
    """Checks if employee_roles present in list allowed_roles.

    Args:
        employee_roles: A list with employee's role names.
        allowed_roles: A tuple with allowed role names.

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
        detail=CharityEmployeesExceptionMsgs.NO_CHARITY_EMPLOYEE_ROLE_PERMISSION.value.format(
            employee_roles=employee_roles,
        ),
    )


def get_allowed_roles_for_employee_role(role_name: str) -> list:
    """Gets list of allowed roles for provided employee role.

    Args:
        role_name: name of employee role.

    Returns:
    list with allowed employee roles.
    """
    try:
        allowed_roles = CharityEmployeeAllowedRolesConstants.ROLES_MAPPING.value[role_name]
    except KeyError:
        raise EmployeeRoleNotSupportedError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=EmployeeRolesExceptionMsgs.ROLE_NOT_SUPPORTED.value.format(
                role_name=role_name,
            )
        )
    return allowed_roles
