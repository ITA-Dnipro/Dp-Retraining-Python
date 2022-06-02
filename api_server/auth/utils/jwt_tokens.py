from datetime import datetime, timedelta

from fastapi import status

from jwt.exceptions import DecodeError, ExpiredSignatureError
import jwt

from auth.utils.exceptions import ExpiredJWTTokenError, JWTTokenError
from common.constants.auth import JWTTokenConstants
from common.exceptions.jwt_tokens import JWTTokenExceptionsMsgs


def create_token_payload(data: str, time_amount: str, time_unit: str) -> dict:
    """Creates payload to be encoded into JWT token.

    Args:
        data: body of future JWT token.
        time_amount: token lifetime amount.
        time_unit: token lifetime unit.

    Returns:
    dict with data and expiration date.
    """
    return {
        'data': data,
        'exp': datetime.now() + timedelta(**{time_unit: time_amount}),
    }


def create_jwt_token(payload: dict, key: str) -> str:
    """Creates JWT token with payload encoded with key.

    Args:
        payload: body of JWT token.
        key: secret used to encode token.

    Returns:
    Encoded JWT token.
    """
    return encode_jwt_token(payload=payload, key=key)


def encode_jwt_token(
        payload: dict,
        key: str,
        algorithm: str = JWTTokenConstants.ALGORITHM_HS512.value,
) -> str:
    """Encodes payload with key to create JWT token.

    Args:
        payload: to encode in JWT token.
        key: for token encoding.
        algorithm: used in JWT token encoding.

    Returns:
    String with encoded JWT token.
    """
    return jwt.encode(
        payload=payload, key=key, algorithm=algorithm,
    ).decode(JWTTokenConstants.ENCODING_UTF_8.value)


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
        raise JWTTokenError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=JWTTokenExceptionsMsgs.INVALID_JWT_TOKEN.value,
        )
    except ExpiredSignatureError:
        raise ExpiredJWTTokenError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=JWTTokenExceptionsMsgs.JWT_TOKEN_EXPIRED.value,
        )
    return payload
