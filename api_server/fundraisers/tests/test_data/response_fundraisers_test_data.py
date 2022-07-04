from unittest.mock import ANY

from charities.tests.test_data import response_charities_test_data
from common.tests.test_data.fundraisers import request_test_fundraise_data
from fundraisers.tests.test_data import response_fundraise_statuses_test_data

# Test data.
RESPONSE_FUNDRAISE_TEST_DATA = {
    'id': ANY,
    'title': 'Buy 100000 MGM-140 ATACMS missiles (M39A1, M48, M57, M57E1) modifications.',
    'description': (
        'Fundraise to buy 100000 MGM-140 ATACMS missiles (M39A1, M48, M57, M57E1) modifications for '
        'M270 and HIMARS platforms.'
    ),
    'goal': 1000000.0,
    'is_donatable': True,
    'ending_at': '2022-10-10T22:00:00',
    'charity': response_charities_test_data.RESPONSE_CHARITY_OUTPUT_SCHEMA_TEST_DATA,
    'statuses': [response_fundraise_statuses_test_data.RESPONSE_FUNDRAISE_STATUS_NEW_TEST_DATA],
}
# GET
RESPONSE_GET_FUNDRAISERS_EMPTY_DB = {
    'data': {
        'current_page': 1,
        'has_next': False,
        'has_previous': False,
        'items': [],
        'next_page': None,
        'previous_page': None,
        'total_pages': 0
    },
    'errors': [],
    'status_code': 200
}
RESPONSE_GET_FUNDRAISERS = {
    'data': {
        'current_page': 1,
        'has_next': False,
        'has_previous': False,
        'items': [RESPONSE_FUNDRAISE_TEST_DATA],
        'next_page': None,
        'previous_page': None,
        'total_pages': 1
    },
    'errors': [],
    'status_code': 200
}
RESPONSE_GET_FUNDRAISE = {
    'data': RESPONSE_FUNDRAISE_TEST_DATA,
    'errors': [],
    'status_code': 200
}
# POST
RESPONSE_POST_FUNDRAISE = {
    'data': RESPONSE_FUNDRAISE_TEST_DATA,
    'errors': [],
    'status_code': 201
}
# Errors.
RESPONSE_FUNDRAISE_NOT_FOUND = {
    'data': [],
    'errors': [{'detail': f"Fundraise with id: '{request_test_fundraise_data.DUMMY_FUNDRAISE_UUID}' not found."}],
    'status_code': 404,
}
RESPONSE_FUNDRAISE_NO_EMPLOYEE_PERMISSION = {
    'data': [],
    'errors': [
        {
            'detail': 'Employee do not have permissions to perform this action.',
        },
    ],
    'status_code': 403
}
