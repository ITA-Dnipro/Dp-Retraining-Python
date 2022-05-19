from unittest.mock import ANY

from common.tests.test_data.users import request_test_user_pictures_data

# GET
RESPONSE_GET_USER_PICTURE = {
    'data': {'id': ANY, 'url': None},
    'errors': [],
    'status_code': 200,
}
# POST
RESPONSE_POST_USER_PICTURES = {
    'data': {'id': ANY, 'url': None},
    'errors': [],
    'status_code': 201,
}
# DELETE
RESPONSE_USER_PICTURE_DELETE = b''
# Errors.
RESPONSE_USER_PICTURE_NOT_FOUND = {
    'data': [],
    'errors': [
        {'detail': f"UserPicture with id: '{request_test_user_pictures_data.DUMMY_USER_PICTURE_UUID}' not found."}
    ],
    'status_code': 404,
}
