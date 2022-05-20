import enum


class AuthExceptionMsgs(enum.Enum):
    """Constants for Auth exception messages."""
    WRONG_USERNAME_OR_PASSWORD = 'Incorrect username or password.'


class EmailConfirmationTokenExceptionMsgs(enum.Enum):
    """Constants for EmailConfirmationToken exception messages."""
    USER_ALREADY_ACTIVATED = "User with email: '{user_email}' already activated."
