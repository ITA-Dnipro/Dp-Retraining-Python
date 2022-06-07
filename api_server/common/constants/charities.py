from enum import Enum


class CharitySchemaConstants(Enum):
    """Charities schema constants."""
    PHONE_REGEX = r"^(?:\+38)?(0\d{9})$"
    EMAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
