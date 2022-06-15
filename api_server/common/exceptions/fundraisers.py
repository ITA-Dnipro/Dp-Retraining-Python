import enum


class FundraiseExceptionMsgs(enum.Enum):
    """Constants for Fundraise exception messages."""
    FUNDRAISE_NOT_FOUND = "Fundraise with {column}: '{value}' not found."
    NO_USER_PERMISSIONS = 'User do not have permissions to perform this action.'
