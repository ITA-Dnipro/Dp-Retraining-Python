import enum


class FundraiseExceptionMsgs(enum.Enum):
    """Constants for Fundraise exception messages."""
    FUNDRAISE_NOT_FOUND = "Fundraise with {column}: '{value}' not found."
