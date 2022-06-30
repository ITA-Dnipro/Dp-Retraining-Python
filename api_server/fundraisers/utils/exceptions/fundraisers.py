from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from common.schemas.responses import ResponseBaseSchema


class FundraiseNotFoundError(HTTPException):
    """Custom Fundraise not found error."""
    pass


class FundraisePermissionError(HTTPException):
    """Custom Fundraise not found error."""
    pass


def fundraise_not_found_error_handler(request: Request, exc: FundraiseNotFoundError):
    """Handler for FundraiseNotFoundError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised FundraiseNotFoundError.

    Returns:
    http response for raised FundraiseNotFoundError.
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


def fundraise_no_permissions_error_handler(request: Request, exc: FundraisePermissionError):
    """Handler for FundraisePermissionError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised FundraisePermissionError.

    Returns:
    http response for raised FundraisePermissionError.
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
