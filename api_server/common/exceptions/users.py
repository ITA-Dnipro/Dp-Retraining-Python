import enum

from common.constants.users import UserServiceConstants


class UserExceptionMsgs(enum.Enum):
    """Constants for Users exception messages."""
    NO_USER_PERMISSIONS = 'User do not have permissions to perform this action.'
    USER_NOT_FOUND = "User with {column}: '{value}' not found."


class UserPictureExceptionMsgs(enum.Enum):
    """Constants for UserPicture exception messages."""
    IMAGE_EXCEED_MAX_SIZE = 'Your image exceed maximum size of 6 megabytes.'
    UNSUPPORTED_IMAGE_EXTENSION = (
        "Your image's extension not supported, please use image with one of the supported extensions: "
        f"{', '.join(UserServiceConstants.VALID_IMAGE_EXTENSIONS.value.keys())}."
    )
    INVALID_IMAGE_RESOLUTION = (
        'The image width or height is outside of supported range. Supported width minimum: {min_width} px, '
        'maximum: {max_width} px.Supported height minimum: {min_height} px, maximum: {max_height} px.'.format(
            min_width=UserServiceConstants.MIN_IMAGE_WIDTH.value,
            max_width=UserServiceConstants.MAX_IMAGE_WIDTH.value,
            min_height=UserServiceConstants.MIN_IMAGE_HEIGHT.value,
            max_height=UserServiceConstants.MAX_IMAGE_HEIGHT.value,
        )
    )
