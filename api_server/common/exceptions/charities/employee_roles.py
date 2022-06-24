import enum


class EmployeeRolesExceptionMsgs(enum.Enum):
    """Constants for Employee roles exception messages."""
    ROLE_NOT_SUPPORTED = "Can not add role with name: '{role_name}' to Employee, role is not supported."
    ROLE_ALREADY_ADDED_TO_EMPLOYEE = "Role with id: '{role_id}' already added to Employee with id: '{employee_id}'."
    ROLE_NOT_FOUND = "EmployeeRole with id: '{role_id}' not found in Employee with id: '{employee_id}'."
