from unittest.mock import ANY

from charities.tests.test_data import response_charity_employees_test_data
from common.tests.test_data.charities import request_test_charity_data
from common.tests.test_data.users import request_test_user_data

# Test data.
RESPONSE_CHARITY_OUTPUT_SCHEMA_TEST_DATA = {
    'description': 'Good deeds charity, making good deeds since 2000.',
    'email': 'good.deeds@totalynotemail.com',
    'id': ANY,
    'phone_number': '+380501112233',
    'title': 'Good deeds charity',
}

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
                'charity_employees': [
                    response_charity_employees_test_data.RESPONSE_CHARITY_EMPLOYEE_SUPERVISOR_TEST_DATA,
                ],
                'fundraisers': [],
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
        'charity_employees': [
            response_charity_employees_test_data.RESPONSE_CHARITY_EMPLOYEE_SUPERVISOR_TEST_DATA,
        ],
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
        'charity_employees': [response_charity_employees_test_data.RESPONSE_CHARITY_EMPLOYEE_SUPERVISOR_TEST_DATA],
        'fundraisers': [],
        'id': ANY,
        'phone_number': '+380501112233',
        'title': 'Good deeds charity'
    },
    'errors': [],
    'status_code': 201
}
# PUT
RESPONSE_PUT_CHARITY = {
    'data': {
        'description': 'Updated Good deeds charity, making good deeds since 2000.',
        'email': 'updated-good.deeds@totalynotemail.com',
        'charity_employees': [response_charity_employees_test_data.RESPONSE_CHARITY_EMPLOYEE_SUPERVISOR_TEST_DATA],
        'fundraisers': [],
        'id': ANY,
        'phone_number': '+380512223344',
        'title': 'Updated Good deeds charity',
    },
    'errors': [],
    'status_code': 200
}
# DELETE
RESPONSE_DELETE_CHARITY = b''
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
RESPONSE_EMPLOYEE_NOT_LISTED_IN_CHARITY_EMPLOYEES = {
    'data': [],
    'errors': [
        {
            'detail': (
                f"User with username: '{request_test_user_data.ADD_USER_TEST_DATA['username']}' not listed as an "
                f"Employee in charity and can not perform this action."
            )
        }
    ],
    'status_code': 403
}
RESPONSE_EMPLOYEE_ROLE_MANAGER_NOT_ENOUGH_PERMISSIONS = {
    'data': [],
    'errors': [
        {
            'detail': "Employee with roles: ['manager'] does not have permission to perform this action."
        }
    ],
    'status_code': 403
}
