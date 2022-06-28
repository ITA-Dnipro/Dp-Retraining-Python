from common.tests.test_data.users import request_test_user_data

ADD_CHARITY_EMPLOYEE_MANAGER_TEST_DATA = {
    'user_email': request_test_user_data.ADD_USER_TEST_DATA['email'],
    'role': 'manager',
}
ADD_CHARITY_EMPLOYEE_SUPERVISOR_TEST_DATA = {
    'user_email': request_test_user_data.ADD_USER_TEST_DATA['email'],
    'role': 'supervisor',
}
