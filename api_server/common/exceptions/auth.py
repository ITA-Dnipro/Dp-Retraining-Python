import enum


class AuthExceptionMsgs(enum.Enum):
    """Constants for Auth exception messages."""
    WRONG_USERNAME_OR_PASSWORD = 'Incorrect username or password.'
