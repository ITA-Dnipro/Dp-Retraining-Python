from fastapi import HTTPException, Request

from starlette.responses import JSONResponse

from common.schemas.responses import ResponseBaseSchema


class CharityNotFoundError(HTTPException):
    """Custom Fundraise not found error."""
    pass


def charity_not_found_error_handler(request: Request, exc: CharityNotFoundError):
    """Handler for CharityNotFoundError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised CharityNotFoundError.

    Returns:
    http response for raised CharityNotFoundError.
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
