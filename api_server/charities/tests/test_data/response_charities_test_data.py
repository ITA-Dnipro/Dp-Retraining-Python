from unittest.mock import ANY

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
