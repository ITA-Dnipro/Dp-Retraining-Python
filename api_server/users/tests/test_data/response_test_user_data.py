from unittest.mock import ANY

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
