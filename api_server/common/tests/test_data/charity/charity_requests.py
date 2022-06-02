import random

EDIT_CHARITY = {
    "description": "Very good organisation",
    "phone_number": "+380408904888",
}

EMPTY_REQUEST = {}

ADDITIONAL_USER_TEST_DATA = {
    'username': 'test_george',
    'first_name': 'george',
    'last_name': 'bar',
    'email': 'test_george@john.com',
    'password': '12345678',
    'phone_number': '+380991112244',
}

DUMMY_UUID = "57c2588b-a744-4a82-837f-4f04ffd4932e"


def add_manager_successfully(manager_mane: str) -> dict:
    return {'data': [{'detail': f'Manager {manager_mane} '
                                'has been successfully added. He is supermanager.'}],
            'errors': [],
            'status_code': 200}


def initialize_charity_data(title: str) -> dict:
    return {"title": title,
            "description": "Some good organisation",
            "phone_number": "+3807078" + str(random.randint(10000, 99999)),
            "organisation_email": "org" + str(random.randint(10000, 99999)) + "@mail.org"
            }


def response_create_organisation_endpoint(user_id) -> dict:
    return {
        "user_id": str(user_id),
        "title": "Charity Organisation",
        "description": "Some good organisation",
        "phone_number": "+380707813196",
        "organisation_email": "org@mail.org"
    }
