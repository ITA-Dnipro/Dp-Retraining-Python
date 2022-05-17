from unittest.mock import ANY

DUMMY_BALANCE_UUID = '7c1b7fb5-20f2-4988-b075-e4cc236f7784'

RESPONSE_BALANCE_TEST_DATA = {
    'id': ANY,
    'amount': ANY,
}
# GET
RESPONSE_BALANCES_EMPTY_DB = {'data': [], 'errors': [], 'status_code': 200}
RESPONSE_GET_BALANCES = {
    'data': [RESPONSE_BALANCE_TEST_DATA],
    'errors': [],
    'status_code': 200,
}
RESPONSE_GET_BALANCE = {
    'data': RESPONSE_BALANCE_TEST_DATA,
    'errors': [],
    'status_code': 200,
}
# Errors.
RESPONSE_BALANCE_NO_PERMISSION = {
    'data': [],
    'errors': [{'detail': 'User don\'t have access to balance with id: "7c1b7fb5-20f2-4988-b075-e4cc236f7784".'}],
    'status_code': 403,
}
