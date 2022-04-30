import enum


class UserModelConstants(enum.Enum):
    """User model constants."""
    # Numerics.
    CHAR_SIZE_64 = 64
    CHAR_SIZE_256 = 256

    # Booleans.
    TRUE = True
    FALSE = False


class UserSchemaConstants(enum.Enum):
    """User schema constants."""
    # Numerics.
    CHAR_SIZE_2 = 2
    СHAR_SIZE_3 = 3
    CHAR_SIZE_6 = 6
    CHAR_SIZE_64 = 64
    CHAR_SIZE_256 = 256

    # Regex.
    EMAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
