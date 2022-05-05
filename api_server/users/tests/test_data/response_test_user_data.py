from unittest.mock import ANY

from common.tests.test_data.users import request_test_user_data

RESPONSE_USER_TEST_DATA = {
    'id': ANY,
    'username': 'test_john',
    'first_name': 'john',
    'last_name': 'bar',
    'email': 'test_john@john.com',
    'phone_number': '+380991112233',
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
# Errors.
RESPONSE_USER_NOT_FOUND = {'detail': f"User with id: '{request_test_user_data.DUMMY_USER_UUID}' not found."}
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
