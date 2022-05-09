from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from common.schemas.responses import ResponseBaseSchema


class UserNotFoundError(HTTPException):
    """Custom User not found error."""
    pass


class UserPermissionError(HTTPException):
    """Custom User permission error."""
    pass


def user_not_found_error_handler(request: Request, exc: UserNotFoundError):
    """Handler for UserNotFoundError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised UserNotFoundError.

    Returns:
    http response for raised UserNotFoundError.
    """
    response = ResponseBaseSchema(
        status_code=exc.status_code,
        data=[],
        errors=[{"detail": exc.detail}],
    ).dict()
    return JSONResponse(
        status_code=exc.status_code,
        content=response,
    )


def user_permission_error_handler(request: Request, exc: UserPermissionError):
    """Handler for UserPermissionError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised UserPermissionError.

    Returns:
    http response for raised UserPermissionError.
    """
    response = ResponseBaseSchema(
        status_code=exc.status_code,
        data=[],
        errors=[{"detail": exc.detail}],
    ).dict()
    return JSONResponse(
        status_code=exc.status_code,
        content=response,
    )
