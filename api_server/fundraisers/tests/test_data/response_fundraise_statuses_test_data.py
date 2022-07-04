from unittest.mock import ANY

RESPONSE_FUNDRAISE_STATUS_NEW_TEST_DATA = {
    'created_at': ANY,
    'id': ANY,
    'name': 'New',
}
# GET
RESPONSE_GET_FUNDRAISE_STATUSES = {
    'data': [RESPONSE_FUNDRAISE_STATUS_NEW_TEST_DATA],
    'errors': [],
    'status_code': 200,
}
RESPONSE_GET_FUNDRAISE_STATUS = {
    'data': RESPONSE_FUNDRAISE_STATUS_NEW_TEST_DATA,
    'errors': [],
    'status_code': 200,
}
