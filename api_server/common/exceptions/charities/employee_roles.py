import enum


class EmployeeRolesExceptionMsgs(enum.Enum):
    """Constants for Employee roles exception messages."""
    ROLE_NOT_SUPPORTED = "Can not add role with name: '{role_name}' to Employee, role is not supported."
    ROLE_ALREADY_ADDED_TO_EMPLOYEE = (
        "Role with {field_name}: '{field_value}' already added to Employee with id: '{employee_id}'."
    )
    ROLE_NOT_FOUND_IN_EMPLOYEE = "EmployeeRole with id: '{role_id}' not found in Employee with id: '{employee_id}'."
    ROLE_NOT_FOUND = "EmployeeRole with {field_name}: '{field_value}' not found."
    EMPLOYEE_ROLE_NON_REMOVABLE_LAST_SUPERVISOR = (
        "EmployeeRole: '{employee_role}' can not be removed from Employee with id: '{employee_id}', "
        "because Charity have only: '{role_count}' {employee_role}."
    )
    EMPLOYEE_ROLE_NON_REMOVABLE_LAST_ROLE = (
        "EmployeeRole: '{employee_role}' can not be removed from Employee with id: '{employee_id}', "
        "because Employee have only: '{role_count}' roles."
    )
