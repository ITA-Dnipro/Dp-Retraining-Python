from unittest.mock import ANY

from charities.tests.test_data import response_employee_roles_test_data
from users.tests.test_data import response_test_user_data

RESPONSE_CHARITY_EMPLOYEE_TEST_DATA = {
    'id': ANY,
    'roles': [response_employee_roles_test_data.RESPONSE_GET_EMPLOYEE_ROLE],
    'user': response_test_user_data.RESPONSE_USER_TEST_DATA
}
# GET
RESPONSE_GET_CHARITY_EMPLOYEES = {
    'data': [RESPONSE_CHARITY_EMPLOYEE_TEST_DATA],
    'errors': [],
    'status_code': 200,
}
RESPONSE_GET_CHARITY_EMPLOYEE = {
    'data': RESPONSE_CHARITY_EMPLOYEE_TEST_DATA,
    'errors': [],
    'status_code': 200,
}
