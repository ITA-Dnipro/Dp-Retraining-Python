from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from common.schemas.responses import ResponseBaseSchema


class FundraiseStatusNotFoundError(HTTPException):
    """Custom FundraiseStatus not found error."""
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
