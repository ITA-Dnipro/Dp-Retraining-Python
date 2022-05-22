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


class EmailConfirmationTokenNotFoundError(HTTPException):
    """Custom EmailConfirmationToken not found exception."""
    pass


class EmailConfirmationTokenExpiredError(HTTPException):
    """Custom EmailConfirmationToken already expired exception."""
    pass


class EmailConfirmationJWTTokenError(HTTPException):
    """Custom EmailConfirmationToken invalid JWT token exception."""
    pass


class EmailConfirmationExpiredJWTTokenError(HTTPException):
    """"""
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


def email_confirmation_token_not_found_error_handler(request: Request, exc: EmailConfirmationTokenNotFoundError):
    """Handler for EmailConfirmationTokenNotFoundError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised EmailConfirmationTokenNotFoundError.

    Returns:
    http response for raised EmailConfirmationTokenNotFoundError.
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


def email_confirmation_token_expired_handler(request: Request, exc: EmailConfirmationTokenExpiredError):
    """Handler for EmailConfirmationTokenExpiredError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised EmailConfirmationTokenExpiredError.

    Returns:
    http response for raised EmailConfirmationTokenExpiredError.
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


def email_confirmation_invalid_jwt_token_handler(request: Request, exc: EmailConfirmationJWTTokenError):
    """Handler for EmailConfirmationJWTTokenError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised EmailConfirmationJWTTokenError.

    Returns:
    http response for raised EmailConfirmationJWTTokenError.
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


def email_confirmation_expired_jwt_token_handler(request: Request, exc: EmailConfirmationExpiredJWTTokenError):
    """Handler for EmailConfirmationExpiredJWTTokenError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised EmailConfirmationExpiredJWTTokenError.

    Returns:
    http response for raised EmailConfirmationExpiredJWTTokenError.
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
