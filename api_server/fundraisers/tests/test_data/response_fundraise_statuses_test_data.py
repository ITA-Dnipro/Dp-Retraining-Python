from unittest.mock import ANY

from common.tests.test_data.fundraisers import request_test_fundraise_status_data

RESPONSE_FUNDRAISE_STATUS_NEW_TEST_DATA = {
    'created_at': ANY,
    'id': ANY,
    'name': 'New',
}
RESPONSE_FUNDRAISE_STATUS_IN_PROGRESS_TEST_DATA = {
    'created_at': ANY,
    'id': ANY,
    'name': 'In progress',
}
RESPONSE_FUNDRAISE_STATUS_ON_HOLD_TEST_DATA = {
    'created_at': ANY,
    'id': ANY,
    'name': 'On hold',
}
RESPONSE_FUNDRAISE_STATUS_COMPLETED_TEST_DATA = {
    'created_at': ANY,
    'id': ANY,
    'name': 'Completed',
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
# POST
RESPONSE_POST_FUNDRAISE_STATUS_IN_PROGRESS = {
    'data': RESPONSE_FUNDRAISE_STATUS_IN_PROGRESS_TEST_DATA,
    'errors': [],
    'status_code': 201,
}
RESPONSE_POST_FUNDRAISE_STATUS_ON_HOLD = {
    'data': RESPONSE_FUNDRAISE_STATUS_ON_HOLD_TEST_DATA,
    'errors': [],
    'status_code': 201,
}
RESPONSE_POST_FUNDRAISE_STATUS_COMPLETED = {
    'data': RESPONSE_FUNDRAISE_STATUS_COMPLETED_TEST_DATA,
    'errors': [],
    'status_code': 201,
}
# Errors
RESPONSE_FUNDRAISE_STATUS_NOT_PERMITTED = {
    'data': [],
    'errors': [
        {
            'detail': "FundraiseStatus with name: 'New' is not permitted."
        }
    ],
    'status_code': 403,
}
RESPONSE_FUNDRAISE_STATUS_NOT_SUPPORTED = {
    'data': [],
    'errors': [
        {
            'detail': (
                f"FundraiseStatus with name: "
                f"'{request_test_fundraise_status_data.ADD_FUNDRAISE_STATUS_NOT_SUPPORTED_TEST_DATA['name']}' "
                f"is not supported."
            )
        }
    ],
    'status_code': 400,
}
