import random

EDIT_CHARITY = {
    "description": "Very good organisation",
    "phone_number": "+380408904888",
}

EMPTY_REQUEST = {}


DUMMY_UUID = "57c2588b-a744-4a82-837f-4f04ffd4932e"


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
