from datetime import datetime, timedelta

from fastapi import status

from jwt.exceptions import DecodeError, ExpiredSignatureError
import jwt

from auth.utils.exceptions import EmailConfirmationExpiredJWTTokenError, EmailConfirmationJWTTokenError
from common.constants.auth import EmailConfirmationTokenConstants
from common.exceptions.auth import EmailConfirmationTokenExceptionMsgs
from users.models import User


def create_email_cofirmation_token(user: User) -> str:
    """Creates JWT token encoded with user's password hash.

    Args:
        user: instance of User object.

    Returns:
    Encoded JWT token.
    """
    payload = create_email_confirmation_token_payload(user)
    return encode_jwt_token(payload=payload, key=user.password)


def create_email_confirmation_token_payload(
        user: User,
        time_amount: str = EmailConfirmationTokenConstants.TOKEN_EXPIRE_7.value,
        time_unit: str = EmailConfirmationTokenConstants.DAYS.value,
) -> dict:
    """Creates payload to be encoded into JWT token.

    Args:
        user: instance of User object.
        time_amount: token lifetime amount.
        time_unit: token lifetime unit.

    Returns:
    dict with user.id and expiration date.
    """
    return {
        'id': str(user.id),
        'exp': datetime.utcnow() + timedelta(**{time_unit: time_amount}),
    }


def encode_jwt_token(
        payload: dict,
        key: str,
        algorightm: str = EmailConfirmationTokenConstants.ALGORITHM_HS512.value,
) -> str:
    """Encodes payload with key to create JWT token.

    Args:
        payload: to encode in JWT token.
        key: for token encoding.
        algorightm: used in JWT token encoding.

    Returns:
    String with encoded JWT token.
    """
    return jwt.encode(
        payload=payload, key=key, algorithm=algorightm,
    ).decode(EmailConfirmationTokenConstants.ENCODING_UTF_8.value)


def decode_jwt_token(token: str, key: str) -> dict:
    """Decodes JWT token and return it's content.

    Args:
        token: Encoded JWT token.

    Raise:
        EmailConfirmationJWTTokenError in case invalid JWT token.

        EmailConfirmationExpiredJWTTokenError in case JWT token expired.

    Returns:
    dict with decoded JWT token.
    """
    try:
        payload = jwt.decode(jwt=token, key=key)
    except DecodeError:
        raise EmailConfirmationJWTTokenError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=EmailConfirmationTokenExceptionMsgs.INVALID_JWT_TOKEN.value,
        )
    except ExpiredSignatureError:
        raise EmailConfirmationExpiredJWTTokenError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=EmailConfirmationTokenExceptionMsgs.JWT_TOKEN_EXPIRED.value,
        )
    return payload
