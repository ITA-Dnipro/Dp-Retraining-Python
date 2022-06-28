from unittest.mock import ANY

from charities.tests.test_data import response_charity_employees_test_data
from common.tests.test_data.charities import request_test_charity_data

# GET
RESPONSE_GET_CHARITIES_EMPTY_DB = {
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
RESPONSE_GET_CHARITIES = {
    'data': {
        'current_page': 1,
        'has_next': False,
        'has_previous': False,
        'items': [
            {
                'description': 'Good deeds charity, making good deeds since 2000.',
                'email': 'good.deeds@totalynotemail.com',
                'id': ANY,
                'phone_number': '+380501112233',
                'title': 'Good deeds charity',
            }
        ],
        'next_page': None,
        'previous_page': None,
        'total_pages': 1
    },
    'errors': [],
    'status_code': 200
}
RESPONSE_GET_CHARITY = {
    'data': {
        'description': 'Good deeds charity, making good deeds since 2000.',
        'email': 'good.deeds@totalynotemail.com',
        'employees': [response_charity_employees_test_data.RESPONSE_GET_CHARITY_EMPLOYEE],
        'fundraisers': [],
        'id': ANY,
        'phone_number': '+380501112233',
        'title': 'Good deeds charity'},
    'errors': [],
    'status_code': 200
}
# POST
RESPONSE_POST_CHARITIES = {
    'data': {
        'description': 'Good deeds charity, making good deeds since 2000.',
        'email': 'good.deeds@totalynotemail.com',
        'employees': [response_charity_employees_test_data.RESPONSE_GET_CHARITY_EMPLOYEE],
        'fundraisers': [],
        'id': ANY,
        'phone_number': '+380501112233',
        'title': 'Good deeds charity'},
    'errors': [],
    'status_code': 201
}
# Errors
RESPONSE_CHARITY_NOT_FOUND = {
    'data': [],
    'errors': [{'detail': f"Charity with id: '{request_test_charity_data.DUMMY_CHARITY_UUID}' not found."}],
    'status_code': 404,
}
RESPONSE_CHARITY_DUPLICATE_EMAIL = {
    'data': [],
    'errors': [
        {'detail': "Charitie with email: 'good.deeds@totalynotemail.com' already exists."}
    ],
    'status_code': 400}