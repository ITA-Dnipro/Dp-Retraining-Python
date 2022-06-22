import enum


class CharityEmployeesExceptionMsgs(enum.Enum):
    """Constants for Charity employee exception messages."""
    EMPLOYEE_ALREADY_IN_CHARITY = 'Employee with id: {employee_id} already added to Charity with id: {charity_id}.'
    NO_EMPLOYEE_IN_CHARITY = (
        "User with username: '{username}' not listed as an Employee in charity and can not perform this action."
    )
    NO_CHARITY_EMPLOYEE_ROLE_PERMISSION = (
        'Employee with roles: {employee_roles} does not have permission to perform this action.'
    )
