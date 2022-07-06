from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from common.schemas.responses import ResponseBaseSchema


class FundraiseStatusNotFoundError(HTTPException):
    """Custom FundraiseStatus not found error."""
    pass


class FundraiseStatusNotSupportedError(HTTPException):
    """Custom FundraiseStatus not supported error."""
    pass


class FundraiseStatusPermissionError(HTTPException):
    """Custom FundraiseStatus permission error."""
    pass


def fundraise_status_not_found_error_handler(request: Request, exc: FundraiseStatusNotFoundError):
    """Handler for FundraiseStatusNotFoundError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised FundraiseStatusNotFoundError.

    Returns:
    http response for raised FundraiseStatusNotFoundError.
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


def fundraise_status_not_supported_error_handler(request: Request, exc: FundraiseStatusNotSupportedError):
    """Handler for FundraiseStatusNotSupportedError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised FundraiseStatusNotSupportedError.

    Returns:
    http response for raised FundraiseStatusNotSupportedError.
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


def fundraise_status_permission_error_handler(request: Request, exc: FundraiseStatusPermissionError):
    """Handler for FundraiseStatusPermissionError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised FundraiseStatusPermissionError.

    Returns:
    http response for raised FundraiseStatusPermissionError.
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
