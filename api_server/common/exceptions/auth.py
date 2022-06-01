import enum


class AuthExceptionMsgs(enum.Enum):
    """Constants for Auth exception messages."""
    WRONG_USERNAME_OR_PASSWORD = 'Incorrect username or password.'


class EmailConfirmationTokenExceptionMsgs(enum.Enum):
    """Constants for EmailConfirmationToken exception messages."""
    USER_ALREADY_ACTIVATED = "User with email: '{user_email}' already activated."
    TOKEN_EXPIRED = 'Email confirmation token alredy expired.'
    TOKEN_CREATION_SPAM = (
        'Cannot create EmailConfirmationToken please check your email inbox and try again in: '
        '{time_amount} {time_units}.'
    )


class ChangePasswordTokenExceptionMsgs(enum.Enum):
    """Constants for ChangePasswordToken exception messages."""
    TOKEN_CREATION_SPAM = (
        'Cannot create ChangePasswordToken please check your email inbox and try again in: {time_amount} {time_units}.'
    )
    TOKEN_EXPIRED = 'Change password token alredy expired.'
