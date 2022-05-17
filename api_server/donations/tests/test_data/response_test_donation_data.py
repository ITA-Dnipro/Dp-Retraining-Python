from unittest.mock import ANY

DUMMY_DONATION_UUID = '7c1b7fb5-20f2-4988-b075-e4cc236f7784'

RESPONSE_DONATION_TEST_DATA = {
    'id': ANY,
    'amount': ANY,
    'recipient_id': ANY,
    'sender_id': ANY,
}
# GET
RESPONSE_DONATIONS_EMPTY_DB = {'data': [], 'errors': [], 'status_code': 200}
RESPONSE_GET_DONATIONS = {
    'data': [RESPONSE_DONATION_TEST_DATA],
    'errors': [],
    'status_code': 200,
}
RESPONSE_GET_DONATION = {
    'data': RESPONSE_DONATION_TEST_DATA,
    'errors': [],
    'status_code': 200,
}
# Errors.
RESPONSE_DONATION_NOT_FOUND = {'detail': f"Donation with id: '{DUMMY_DONATION_UUID}' not found."}
