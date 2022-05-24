EDIT_CHARITY = {
    "description": "Very good organisation",
    "phone_number": "+380408904888",
}

CHARITY_INIT = {"title": "Charity Organisation",
                "description": "Some good organisation",
                "phone_number": "+380707813196",
                "organisation_email": "org@mail.org"
                }
EMPTY_REQUEST = {}


def response_create_organisation_endpoint(user_id) -> dict:
    return {
        "user_id": str(user_id),
        "title": "Charity Organisation",
        "description": "Some good organisation",
        "phone_number": "+380707813196",
        "organisation_email": "org@mail.org"
    }


