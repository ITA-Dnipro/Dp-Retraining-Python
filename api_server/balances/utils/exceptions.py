"""Balance exceptions module."""
from fastapi import HTTPException


class BalanceNotFoundError(HTTPException):
    """Custom Balance not found error."""
    pass


class BalancePermissionError(HTTPException):
    """Custom Balance permission error."""
    pass
