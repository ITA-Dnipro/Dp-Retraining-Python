from common.tests.test_data.users.request_test_user_data import ADD_USER_TEST_DATA

# POST.
POST_FORGOT_PASSWORD_VALID_EMAIL = {
    'email': ADD_USER_TEST_DATA['email'],
}
POST_CHANGE_PASSWORD_VALID_PAYLOAD = {
    'token': '',
    'password': '654321',
}
