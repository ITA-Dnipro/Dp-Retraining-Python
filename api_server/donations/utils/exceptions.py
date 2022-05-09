"""Donations exceptions module."""
from fastapi import HTTPException


class DonationNotFoundError(HTTPException):
    """Custom Donation not found error."""
    pass


class DonationPermissionError(HTTPException):
    """Custom Donation permission error."""
    pass
