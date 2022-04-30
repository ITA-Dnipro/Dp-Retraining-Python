"""User exceptions module."""
from fastapi import HTTPException


class UserNotFoundError(HTTPException):
    pass
