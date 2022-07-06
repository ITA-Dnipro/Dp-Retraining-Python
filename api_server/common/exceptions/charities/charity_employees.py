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
    EMPLOYEE_NOT_FOUND = (
        "Employee with {field_name}: '{field_value}' not found in Charity with id: '{charity_id}'."
    )
    EMPLOYEE_NON_REMOVABLE = (
        "Employee with role: '{employee_role}' can not be removed from Charity with id: '{charity_id}', "
        "because Charity have only: '{role_count}' {employee_role}."
    )
