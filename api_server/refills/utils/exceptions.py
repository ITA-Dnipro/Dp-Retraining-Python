"""Refills exceptions module."""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from common.schemas.responses import ResponseBaseSchema


class RefillNotFoundError(HTTPException):
    """Custom Refill not found error."""
    pass


class RefillPermissionError(HTTPException):
    """Custom Refill permission error."""
    pass


def refill_permission_error_handler(request: Request, exc: RefillPermissionError):
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
