from common.tests.test_data.users.request_test_user_data import ADD_USER_TEST_DATA

# POST.
POST_EMAIL_CONFIRMATION_VALID_EMAIL = {
    'email': ADD_USER_TEST_DATA['email'],
}
POST_EMAIL_CONFIRMATION_INVALID_EMAIL = {
    'email': 'nonregisteredemail@totalynotemail.com',
}
# GET.
GET_EMAIL_CONFIRMATION_VALID_TOKEN = {
    'token': ''
}
