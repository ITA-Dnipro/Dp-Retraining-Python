from common.tests.test_data.users.request_test_user_data import ADD_USER_TEST_DATA

LOGIN_VALID_USER_CREDENTIALS = {
    'username': ADD_USER_TEST_DATA['username'],
    'password': ADD_USER_TEST_DATA['password'],
}
LOGIN_INVALID_USER_PASSWORD = {
    'username': ADD_USER_TEST_DATA['username'],
    'password': 'something_totally_wrong',
}
