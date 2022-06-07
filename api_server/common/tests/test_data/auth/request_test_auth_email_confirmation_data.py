from datetime import datetime, timedelta

from auth.models import EmailConfirmationToken
from common.constants.auth.email_confirmation_tokens import EmailConfirmationTokenConstants
from common.tests.test_data.users.request_test_user_data import ADD_USER_TEST_DATA

# POST.
POST_EMAIL_CONFIRMATION_VALID_EMAIL = {
    'email': ADD_USER_TEST_DATA['email'],
}
POST_EMAIL_CONFIRMATION_INVALID_EMAIL = {
    'email': 'nonregisteredemail@totalynotemail.com',
}
# GET.
GET_EMAIL_CONFIRMATION_VALID_TOKEN = {
    'token': ''
}
# Fixtures data.
DATE_TIME_30_MIN_AGO = datetime.now() - timedelta(**EmailConfirmationTokenConstants.TIMEDELTA_30_MIN.value)
EMAIL_CONFIRMATION_TOKEN_MOCK_CREATED_AT_DATA = {
    'time_to_freeze': DATE_TIME_30_MIN_AGO,
    'model': EmailConfirmationToken,
    'field': EmailConfirmationToken.created_at,
    'tick': False,
}
