import enum


class FundraiseExceptionMsgs(enum.Enum):
    """Constants for Fundraise exception messages."""
    FUNDRAISE_NOT_FOUND = "Fundraise with {column}: '{value}' not found."
    NO_EMPLOYEE_PERMISSIONS = 'Employee do not have permissions to perform this action.'
