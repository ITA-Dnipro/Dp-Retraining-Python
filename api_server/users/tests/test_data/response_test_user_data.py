from unittest.mock import ANY

from common.tests.test_data.users import request_test_user_data

RESPONSE_USER_TEST_DATA = {
    'id': ANY,
    'username': 'test_john',
    'first_name': 'john',
    'last_name': 'bar',
    'email': 'test_john@john.com',
    'phone_number': '+380991112233',
    'balance_id': ANY,
}
# GET
RESPONSE_USERS_EMPTY_DB = {'data': [], 'errors': [], 'status_code': 200}
RESPONSE_GET_USERS = {
    'data': [RESPONSE_USER_TEST_DATA],
    'errors': [],
    'status_code': 200,
}
RESPONSE_GET_USER = {
    'data': RESPONSE_USER_TEST_DATA,
    'errors': [],
    'status_code': 200,
}
# POST
RESPONSE_POST_USER = {
    'data': RESPONSE_USER_TEST_DATA,
    'errors': [],
    'status_code': 201,
}
# PUT
RESPONSE_USER_UPDATE_TEST_DATA = {
    'data': {
        'id': ANY,
        'username': request_test_user_data.UPDATE_USER_TEST_DATA['username'],
        'first_name': request_test_user_data.UPDATE_USER_TEST_DATA['first_name'],
        'last_name': request_test_user_data.UPDATE_USER_TEST_DATA['last_name'],
        'email': request_test_user_data.UPDATE_USER_TEST_DATA['email'],
        'phone_number': request_test_user_data.UPDATE_USER_TEST_DATA['phone_number'],
        'balance_id': ANY,
    },
    'errors': [],
    'status_code': 200,
}
# Errors.
RESPONSE_USER_NOT_FOUND = {
    'data': [],
    'errors': [{'detail': "User with id: '7c1b7fb5-20f2-4988-b075-e4cc236f7784' not found."}],
    'status_code': 404,
}
RESPONSE_USER_INVALID_PAYLOAD = {
    'detail': [
        {
            'loc': ['body', 'username'],
            'msg': 'field required',
            'type': 'value_error.missing'
        },
        {
            'loc': ['body', 'email'],
            'msg': 'field required',
            'type': 'value_error.missing'
        },
        {
            'loc': ['body', 'phone_number'],
            'msg': 'field required',
            'type': 'value_error.missing'
        },
        {
            'loc': ['body', 'password'],
            'msg': 'field required',
            'type': 'value_error.missing'
        }
    ]
}
RESPONSE_USER_DUPLICATE_USERNAME = {
    'data': [],
    'errors': [
        {'detail': f'''User with username: '{request_test_user_data.ADD_USER_TEST_DATA["username"]}' already exists.'''}
    ],
    'status_code': 400,
}
RESPONSE_USER_UNAUTHORIZED_UPDATE = {
    'data': [],
    'errors': [{'detail': 'Missing cookie access_token_cookie'}],
    'status_code': 401,
}
RESPONSE_USER_UNAUTHORIZED_UPDATE = {
    'data': [],
    'errors': [{'detail': 'User do not have permissions to perform this action.'}],
    'status_code': 401,
}
RESPONSE_USER_DELETE = b''
RESPONSE_USER_UNAUTHORIZED_DELETE = {
    'data': [],
    'errors': [{'detail': 'User do not have permissions to perform this action.'}],
    'status_code': 401,
}
