from starlette.responses import JSONResponse

from common.schemas.responses import ResponseBaseSchema
from fastapi import HTTPException, Request


class OrganisationHTTPException(HTTPException):
    """Custom Organisation not exception."""
    pass


def organisation_exception_handler(request: Request, exc: OrganisationHTTPException):
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
