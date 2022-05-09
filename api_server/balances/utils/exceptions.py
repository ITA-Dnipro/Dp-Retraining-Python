"""Balance exceptions module."""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from common.schemas.responses import ResponseBaseSchema


class BalanceNotFoundError(HTTPException):
    """Custom Balance not found error."""
    pass


class BalancePermissionError(HTTPException):
    """Custom Balance permission error."""
    pass


def balance_permission_error_handler(request: Request, exc: BalancePermissionError):
    """Handler for BalancePermissionError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised BalancePermissionError.

    Returns:
    http response for raised BalancePermissionError.
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


def balance_not_found_error_handler(request: Request, exc: BalanceNotFoundError):
    """Handler for BalanceNotFoundError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised BalanceNotFoundError.

    Returns:
    http response for raised BalanceNotFoundError.
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
