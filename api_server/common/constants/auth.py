import enum


class AuthJWTConstants(enum.Enum):
    """Auth JWT constants."""
    ALGORITHM_HS256 = 'HS256'
    ACCESS_TOKEN_NAME = 'access'
    REFRESH_TOKEN_NAME = 'refresh'
    # Time units.
    DAYS = 'days'
    MINUTES = 'minutes'
    SECONDS = 'seconds'
    TOKEN_EXPIRE_7 = 7
    TOKEN_EXPIRE_30 = 30
    TOKEN_EXPIRE_60 = 60
    ACCESS_TOKEN_COOKIE_NAME = 'access_token_cookie'
    REFRESH_TOKEN_COOKIE_NAME = 'refresh_token_cookie'
    LOGOUT_MSG = 'Successfully logout.'


class EmailConfirmationTokenModelConstants(enum.Enum):
    """EmailConfirmationToken model constants."""
    CHAR_SIZE_2048 = 2048


class EmailConfirmationTokenSchemaConstants(enum.Enum):
    """EmailConfirmationToken schema constants."""
    # Numerics.
    CHAR_SIZE_2 = 2
    CHAR_SIZE_3 = 3
    CHAR_SIZE_6 = 6
    CHAR_SIZE_64 = 64
    CHAR_SIZE_256 = 256

    # Regex.
    EMAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class EmailConfirmationTokenConstants(enum.Enum):
    """EmailConfirmationToken constants."""

    ALGORITHM_HS512 = 'HS512'
    ENCODING_UTF_8 = 'UTF-8'

    # Time units.
    DAYS = 'days'
    MINUTES = 'minutes'
    SECONDS = 'seconds'
    TOKEN_EXPIRE_7 = 7
