from enum import Enum


class EmployeeRoleModelConstants(Enum):
    """EmployeeRole model constants."""
    CHAR_SIZE_256 = 256


class EmployeeRoleSchemaConstants(Enum):
    """EmployeeRole schema constants."""
    CHAR_SIZE_2 = 2
    CHAR_SIZE_256 = 256


class EmployeeRoleServiceConstants(Enum):
    """EmployeeRole Service constants."""
    SUCCESSFUL_EMPLOYEE_ROLE_REMOVAL_MSG = {
        'message': "EmployeeRole with id: '{role_id}' successfully removed from Employee with id: '{employee_id}'."
    }
