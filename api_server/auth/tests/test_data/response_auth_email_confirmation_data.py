from unittest.mock import ANY

from common.tests.test_data.users import request_test_user_data

# POST
POST_VALID_RESPONSE_EMAIL_CONFIRMATION_TOKEN_TEST_DATA = {
    'data': {
        'id': ANY,
        'token': ANY,
    },
    'errors': [],
    'status_code': 201
}
# GET
GET_VALID_RESPONSE_EMAIL_CONFIRMATION_TOKEN_TEST_DATA = {
    'data': {
        'message': f"User with email: '{request_test_user_data.ADD_USER_TEST_DATA['email']}' successfully "'activated.'
    },
    'errors': [],
    'status_code': 200
}
# Errors.
RESPONSE_EMAIL_CONFIRMATION_USER_EMAIL_NOT_FOUND = {
    'data': [],
    'errors': [
        {'detail': 'User with email: '"'nonregisteredemail@totalynotemail.com' not found."}
    ],
    'status_code': 404
}
GET_EMAIL_CONFIRMATION_USER_ALREADY_ACTIVATED = {
    'data': [],
    'errors': [
        {'detail': f"User with email: '{request_test_user_data.ADD_USER_TEST_DATA['email']}' already "'activated.'}
    ],
    'status_code': 400
}
POST_EMAIL_CONFIRMATION_ANTI_SPAM_TEST_DATA = {
    'data': [],
    'errors': [
        {'detail': 'Cannot create EmailConfirmationToken please check your email inbox and try again in: 5 minutes.'}
    ],
    'status_code': 400
}
