from charities.utils.exceptions.charities import CharityNotFoundError, charity_not_found_error_handler
from charities.utils.exceptions.charity_employees import (
    CharityEmployeeDuplicateError,
    CharityEmployeeNotFoundError,
    CharityEmployeePermissionError,
    CharityNonRemovableEmployeeError,
    charity_employee_not_found_error_handler,
    charity_employee_permission_error_handler,
    charity_non_removable_employee_error_handler,
    employee_already_added_to_charity_error_handler,
)
from charities.utils.exceptions.employee_roles import (
    CharityEmployeeRoleDuplicateError,
    CharityEmployeeRolePermissionError,
    EmployeeRoleNotFoundError,
    EmployeeRoleNotSupportedError,
    charity_employee_role_permission_error_handler,
    employee_role_already_added_to_employee_error_handler,
    employee_role_not_found_error_handler,
    employee_role_not_supported_error_handler,
)

__all__ = [
    'CharityEmployeePermissionError',
    'CharityEmployeeRolePermissionError',
    'CharityNotFoundError',
    'charity_employee_permission_error_handler',
    'charity_employee_role_permission_error_handler',
    'charity_not_found_error_handler',
    'CharityEmployeeDuplicateError',
    'employee_already_added_to_charity_error_handler',
    'EmployeeRoleNotSupportedError',
    'employee_role_not_supported_error_handler',
    'CharityEmployeeRoleDuplicateError',
    'employee_role_already_added_to_employee_error_handler',
    'CharityEmployeeNotFoundError',
    'charity_employee_not_found_error_handler',
    'CharityNonRemovableEmployeeError',
    'charity_non_removable_employee_error_handler',
    'EmployeeRoleNotFoundError',
    'employee_role_not_found_error_handler',
]
