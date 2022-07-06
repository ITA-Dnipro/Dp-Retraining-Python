from common.tests.test_data.users import request_test_user_data

ADD_CHARITY_EMPLOYEE_MANAGER_TEST_DATA = {
    'user_email': request_test_user_data.ADD_USER_TEST_DATA['email'],
    'role': 'manager',
}
ADD_CHARITY_EMPLOYEE_SUPERVISOR_TEST_DATA = {
    'user_email': request_test_user_data.ADD_USER_TEST_DATA['email'],
    'role': 'supervisor',
}
DUMMY_CHARITY_EMPLOYEE_UUID = '4c1b7fb5-30f2-4958-b075-e4cc236f5522'
