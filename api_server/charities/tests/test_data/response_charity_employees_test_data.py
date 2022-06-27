from unittest.mock import ANY

from charities.tests.test_data import response_employee_roles_test_data
from users.tests.test_data import response_test_user_data

RESPONSE_GET_CHARITY_EMPLOYEE = {
    'id': ANY,
    'roles': [response_employee_roles_test_data.RESPONSE_GET_EMPLOYEE_ROLE],
    'user': response_test_user_data.RESPONSE_USER_TEST_DATA
}
