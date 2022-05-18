from unittest.mock import ANY

from users.tests.test_data.response_test_user_data import \
    RESPONSE_USER_TEST_DATA

RESPONSE_VALID_LOGIN_DATA = {
    'data': {
        'access_token': ANY,
        'refresh_token': ANY,
    },
    'errors': [],
    'status_code': 200,
}
RESPONSE_INVALID_LOGIN_PASSWORD = {
    'data': [],
    'errors': [{'detail': 'Incorrect username or password.'}],
    'status_code': 401,
}
RESPONSE_VALID_ME_DATA = {
    'data': RESPONSE_USER_TEST_DATA,
    'errors': [],
    'status_code': 200,
}
RESPONSE_NO_ACCESS_COOKIES = {
    'data': [],
    'errors': [{'detail': 'Missing cookie access_token_cookie'}],
    'status_code': 401
}
RESPONSE_POST_VALID_LOGOUT = {
    'data': {'message': 'Successfully logout.'},
    'errors': [],
    'status_code': 200
}
RESPONSE_VALID_REFRESH_DATA = {
    'data': {
        'access_token': ANY,
        'refresh_token': ANY,
    },
    'errors': [],
    'status_code': 200,
}
RESPONSE_NO_REFRESH_COOKIES = {
    'data': [],
    'errors': [{'detail': 'Missing cookie refresh_token_cookie'}],
    'status_code': 401
}
