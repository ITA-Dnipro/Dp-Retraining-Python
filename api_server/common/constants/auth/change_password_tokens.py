import enum


class ChangePasswordTokenModelConstants(enum.Enum):
    """ChangePasswordToken model constants."""
    CHAR_SIZE_2048 = 2048


class ChangePasswordTokenSchemaConstants(enum.Enum):
    """ChangePasswordToken schema constants."""
    # Numerics.
    CHAR_SIZE_2 = 2
    CHAR_SIZE_3 = 3
    CHAR_SIZE_6 = 6
    CHAR_SIZE_64 = 64
    CHAR_SIZE_256 = 256
    CHAR_SIZE_2048 = 2048

    # Regex.
    EMAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class ChangePasswordTokenConstants(enum.Enum):
    """EmailConfirmationToken constants."""

    ALGORITHM_HS512 = 'HS512'
    ENCODING_UTF_8 = 'UTF-8'

    # Time units.
    DAYS = 'days'
    MINUTES = 'minutes'
    SECONDS = 'seconds'
    TOKEN_EXPIRE_1 = 1
    ONE_SECOND = 1
    MIN_TOKEN_LIFETIME = 5
    MIN_TOKEN_LIFETIME_TIMEDELTA = {MINUTES: MIN_TOKEN_LIFETIME}

    # Responses.
    SUCCESSFUL_CHANGE_PASSWORD_MSG = {'message': "User with email: '{email}' successfully changed password."}
