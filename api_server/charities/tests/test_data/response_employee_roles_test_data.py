from unittest.mock import ANY

RESPONSE_EMPLOYEE_ROLE_SUPERVISOR_TEST_DATA = {
    'id': ANY,
    'name': 'supervisor',
}
RESPONSE_EMPLOYEE_ROLE_MANAGER_TEST_DATA = {
    'id': ANY,
    'name': 'manager',
}
# GET
RESPONSE_GET_EMPLOYEE_ROLES_SUPERVISOR_ROLE = {
    'data': [RESPONSE_EMPLOYEE_ROLE_SUPERVISOR_TEST_DATA],
    'errors': [],
    'status_code': 200
}
RESPONSE_GET_EMPLOYEE_ROLE_SUPERVISOR_ROLE = {
    'data': RESPONSE_EMPLOYEE_ROLE_SUPERVISOR_TEST_DATA,
    'errors': [],
    'status_code': 200
}
# Errors
RESPONSE_EMPLOYEE_ROLES_ROLE_NOT_FOUND_IN_EMPLOYEE = {
    'data': [],
    'errors': [
        {
            'detail': "EmployeeRole with id: '{role_id}' not found in Employee with id: '{employee_id}'."
        }
    ],
    'status_code': 404
}
