UNAUTHORIZED = {'status_code': 401, 'data': [], 'errors': [{'detail': 'Missing cookie access_token_cookie'}]}

NOT_VALID_REQUEST = {'data': [],
                     'errors': [{'detail': 'No valid request has been passed'}],
                     'status_code': 400}
NOT_PERMITTED = {
    "status_code": 403,
    "data": [],
    "errors": [
        {
            "detail": "You do not have permission to perform this action"
        }
    ]
}

SUCCESSFUL_CHARITY_DELETION = {'data': {'detail': 'Organisation has been deleted successfully.'},
                               'errors': [],
                               'status_code': 200}

NOT_FOUND = {'data': [],
             'errors': [{'detail': "This organisation hasn't been found"}],
             'status_code': 404}


def get_successful_organisation_creating(org_id) -> dict:
    return {'data': [{'title': 'Charity Organisation',
                      'description': 'Some good organisation',
                      'organisation_email': 'org@mail.org',
                      'phone_number': '+380707813196',
                      'id': str(org_id)}],
            'errors': [],
            'status_code': 201}


def get_full_charity_description(org_id) -> dict:
    return {'data': [{'description': 'Some good organisation',
                      'id': str(org_id),
                      'organisation_email': 'org@mail.org',
                      'phone_number': '+380707813196',
                      'title': "Charity Organisation"}],
            'errors': [],
            'status_code': 200}


def get_charities_list(title_list: [list, tuple]) -> dict:
    return {'data': [{'description': 'Some good organisation',
                      'title': title} for title in title_list],
            'errors': [],
            'status_code': 200}


def get_successfully_edited_charity_data(org_id):
    return {'data': [{'description': 'Very good organisation',
                      'id': str(org_id),
                      'organisation_email': 'org@mail.org',
                      'phone_number': '+380408904888',
                      'title': 'Charity Organisation'}],
            'errors': [],
            'status_code': 200}
