from unittest.mock import ANY

from common.tests.test_data.users import request_test_user_data

# POST
POST_VALID_RESPONSE_FORGOT_PASSWORD_TOKEN_TEST_DATA = {
    'data': {
        'id': ANY,
        'token': ANY,
    },
    'errors': [],
    'status_code': 201
}
POST_VALID_RESPONSE_CHANGE_PASSWORD_TOKEN_TEST_DATA = {
    'data': {
        'message': (
            f"User with email: '{request_test_user_data.ADD_USER_TEST_DATA['email']}' successfully changed password."
        )
    },
    'errors': [],
    'status_code': 200
}
# Errors.
POST_FORGOT_PASSWORD_ANTI_SPAM_TEST_DATA = {
    'data': [],
    'errors': [
        {'detail': 'Cannot create ChangePasswordToken please check your email inbox and try again in: 5 minutes.'}
    ],
    'status_code': 400
}
POST_CHANGE_PASSWORD_TOKEN_EXPIRED_IN_DB_TEST_DATA = {
    'data': [],
    'errors': [{'detail': 'Change password token alredy expired.'}],
    'status_code': 400
}
POST_CHANGE_PASSWORD_TOKEN_EXPIRED_IN_JWT_TEST_DATA = {
    'data': [],
    'errors': [{'detail': 'Provided JWT token already expired.'}],
    'status_code': 400
}
