"""User exceptions module."""
from fastapi import HTTPException


class UserNotFoundError(HTTPException):
    """Custom User not found error."""
    pass


class UserPermissionError(HTTPException):
    """Custom User permission error."""
    pass
