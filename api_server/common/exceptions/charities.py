import enum


class CharityExceptionMsgs(enum.Enum):
    """Constants for Charity exception messages."""
    CHARITY_NOT_FOUND = "Charity with {column}: '{value}' not found."
    NO_CHARITY_EMPLOYEE_PERMISSION = 'Employee does not have permission to perform this action.'
    NO_CHARITY_EMPLOYEE_ROLE_PERMISSION = (
        'Employee with roles: {employee_roles} does not have permission to perform this action.'
    )
