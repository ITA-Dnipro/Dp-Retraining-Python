from enum import Enum


class CharitySchemaConstants(Enum):
    """Charities schema constants."""
    PHONE_REGEX = r"^(?:\+38)?(0\d{9})$"
    EMAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class CharityModelConstants(Enum):
    """Charities model constants."""
    CHAR_SIZE_128 = 128
    CHAR_SIZE_256 = 256
    CHAR_SIZE_512 = 512
    CHAR_SIZE_8192 = 8192
