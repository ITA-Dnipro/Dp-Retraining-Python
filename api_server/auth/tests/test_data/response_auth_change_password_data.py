from unittest.mock import ANY

# POST
POST_VALID_RESPONSE_CHANGE_PASSWORD_TOKEN_TEST_DATA = {
    'data': {
        'id': ANY,
        'token': ANY,
    },
    'errors': [],
    'status_code': 201
}
# Errors.
POST_CHANGE_PASSWORD_ANTI_SPAM_TEST_DATA = {
    'data': [],
    'errors': [
        {'detail': 'Cannot create ChangePasswordToken please check your email inbox and try again in: 5 minutes.'}
    ],
    'status_code': 400
}
