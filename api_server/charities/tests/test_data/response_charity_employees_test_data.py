from unittest.mock import ANY

from charities.tests.test_data import response_employee_roles_test_data
from users.tests.test_data import response_test_user_data

RESPONSE_CHARITY_EMPLOYEE_SUPERVISOR_TEST_DATA = {
    'id': ANY,
    'roles': [response_employee_roles_test_data.RESPONSE_EMPLOYEE_ROLE_SUPERVISOR_TEST_DATA],
    'user': response_test_user_data.RESPONSE_USER_TEST_DATA
}
RESPONSE_CHARITY_EMPLOYEE_MANAGER_TEST_DATA = {
    'id': ANY,
    'roles': [response_employee_roles_test_data.RESPONSE_EMPLOYEE_ROLE_MANAGER_TEST_DATA],
    'user': response_test_user_data.RESPONSE_USER_TEST_DATA
}
# GET
RESPONSE_GET_CHARITY_EMPLOYEES_SUPERVISOR_ROLE = {
    'data': [RESPONSE_CHARITY_EMPLOYEE_SUPERVISOR_TEST_DATA],
    'errors': [],
    'status_code': 200,
}
RESPONSE_GET_CHARITY_EMPLOYEE_SUPERVISOR_ROLE = {
    'data': RESPONSE_CHARITY_EMPLOYEE_SUPERVISOR_TEST_DATA,
    'errors': [],
    'status_code': 200,
}
# POST
RESPONSE_POST_CHARITY_EMPLOYEES_MANAGER_ROLE = {
    'data': RESPONSE_CHARITY_EMPLOYEE_MANAGER_TEST_DATA,
    'errors': [],
    'status_code': 201,
}
# DELETE
RESPONSE_DELETE_CHARITY_EMPLOYEE_VALID_REMOVAL_MSG = {
    'data': {
        'message': "Employee with id: '{employee_id}' successfully removed from Charity with id: '{charity_id}'."
    },
    'errors': [],
    'status_code': 200
}
# Errors
RESPONSE_CHARITY_EMPLOYEES_ALREADY_ADDED = {
    'data': [],
    'errors': [
        {
            'detail': 'Employee with id: {employee_id} already added to Charity with id: {charity_id}.'
        }
    ],
    'status_code': 400
}
RESPONSE_EMPLOYEE_ROLE_MANAGER_NOT_ENOUGH_PERMISSIONS = {
    'data': [],
    'errors': [
        {
            'detail': "Employee with roles: ['manager'] does not have permission to perform this action."
        }
    ],
    'status_code': 403
}
RESPONSE_CHARITY_EMPLOYEE_LAST_SUPERVISOR_IN_CHARITY = {
    'data': [],
    'errors': [
        {
            'detail': (
                "Employee with role: 'supervisor' can not be removed from Charity with id: '{charity_id}', "
                "because Charity have only: '1' supervisor."
            )
        }
    ],
    'status_code': 403
}
RESPONSE_CHARITY_EMPLOYEE_NOT_FOUND_IN_CHARITY = {
    'data': [],
    'errors': [
        {
            'detail': "Employee with id: '{employee_id}' not found in Charity with id: '{charity_id}'."
        }
    ],
    'status_code': 404
}
