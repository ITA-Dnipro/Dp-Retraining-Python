import enum


class CharityExceptionMsgs(enum.Enum):
    """Constants for Charity exception messages."""
    CHARITY_NOT_FOUND = "Charity with {column}: '{value}' not found."
