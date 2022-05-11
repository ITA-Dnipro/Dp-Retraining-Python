import enum


class UserExceptionMsgs(enum.Enum):
    """Constants for Users exception messages."""
    NO_USER_PERMISSIONS = 'User do not have permissions to perform this action.'


class UserPictureExceptionMsgs(enum.Enum):
    """Constants for UserPicture exception messages."""
    IMAGE_EXCEED_MAX_SIZE = 'Your image exceed maximum size of 6 megabytes.'
