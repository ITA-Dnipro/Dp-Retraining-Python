from fastapi import HTTPException, Request

from starlette.responses import JSONResponse

from common.schemas.responses import ResponseBaseSchema


class OrganisationHTTPException(HTTPException):
    """Custom Organisation not exception."""
    pass


def organisation_exception_handler(request: Request, exc: OrganisationHTTPException):
    """Handler for OrganisationHTTPException exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised OrganisationHTTPException.

    Returns:
        http response for raised OrganisationHTTPException.
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
