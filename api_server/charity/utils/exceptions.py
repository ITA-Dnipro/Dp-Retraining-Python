from fastapi import HTTPException


class OrganisationNotFoundError(HTTPException):
    """Custom Organisation not found error."""
    pass
