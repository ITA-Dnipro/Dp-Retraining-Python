from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from fastapi_jwt_auth.exceptions import AuthJWTException

from common.schemas.responses import ResponseBaseSchema


def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    """Handler for AuthJWTException exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised AuthJWTException.

    Returns:
    http response for raised AuthJWTException.
    """
    response = ResponseBaseSchema(
        status_code=exc.status_code,
        data=[],
        errors=[{"detail": exc.message}],
    ).dict()
    return JSONResponse(
        status_code=exc.status_code,
        content=response,
    )


class AuthUserInvalidPasswordException(HTTPException):
    """Custom User invalid password exception."""
    pass


def invalid_auth_credentials_handler(request: Request, exc: AuthUserInvalidPasswordException):
    """Handler for AuthUserInvalidPasswordException exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised AuthUserInvalidPasswordException.

    Returns:
    http response for raised AuthUserInvalidPasswordException.
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


class UserAlreadyActivatedException(HTTPException):
    """Custom User alredy activated exception."""
    pass


def user_already_activated_handler(request: Request, exc: UserAlreadyActivatedException):
    """Handler for UserAlreadyActivatedException exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised UserAlreadyActivatedException.

    Returns:
    http response for raised UserAlreadyActivatedException.
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
