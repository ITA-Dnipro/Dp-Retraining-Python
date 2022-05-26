from datetime import datetime, timedelta

import jwt

from common.constants.auth import ChangePasswordTokenConstants
from users.models import User


def create_change_password_token(user: User) -> str:
    """Creates change password JWT token encoded with user's password hash.

    Args:
        user: instance of User object.

    Returns:
    Encoded JWT token.
    """
    payload = create_change_password_token_payload(
        user,
        time_amount=ChangePasswordTokenConstants.TOKEN_EXPIRE_1.value,
        time_unit=ChangePasswordTokenConstants.DAYS.value
    )
    return encode_change_password_jwt_token(payload=payload, key=user.password)


def create_change_password_token_payload(
        user: User,
        time_amount: str,
        time_unit: str,
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


def encode_change_password_jwt_token(
        payload: dict,
        key: str,
        algorightm: str = ChangePasswordTokenConstants.ALGORITHM_HS512.value,
) -> str:
    """Encodes payload with key to create change password JWT token.

    Args:
        payload: to encode in JWT token.
        key: for token encoding.
        algorightm: used in JWT token encoding.

    Returns:
    String with encoded JWT token.
    """
    return jwt.encode(
        payload=payload, key=key, algorithm=algorightm,
    ).decode(ChangePasswordTokenConstants.ENCODING_UTF_8.value)
