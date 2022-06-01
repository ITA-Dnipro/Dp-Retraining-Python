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
    LOGOUT_MSG = {'message': 'Successfully logout.'}
    TOKEN_LIFTETIME_60_MINUTES = {MINUTES: TOKEN_EXPIRE_30}
    TOKEN_LIFETIME_7_DAYS = {DAYS: TOKEN_EXPIRE_7}
