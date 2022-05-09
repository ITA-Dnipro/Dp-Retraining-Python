from unittest.mock import ANY

DUMMY_REFILL_UUID = '7c1b7fb5-20f2-4988-b075-e4cc236f7784'

RESPONSE_REFILL_TEST_DATA = {
    'id': ANY,
    'amount': ANY,
    'balance_id': ANY,
}
# GET
RESPONSE_REFILLS_EMPTY_DB = {'data': [], 'errors': [], 'status_code': 200}
RESPONSE_GET_REFILLS = {
    'data': [RESPONSE_REFILL_TEST_DATA],
    'errors': [],
    'status_code': 200,
}
RESPONSE_GET_REFILL = {
    'data': RESPONSE_REFILL_TEST_DATA,
    'errors': [],
    'status_code': 200,
}
# Errors.
RESPONSE_REFILL_NOT_FOUND = {'detail': f"Refill with id: '{DUMMY_REFILL_UUID}' not found."}
