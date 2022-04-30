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
