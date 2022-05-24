from fastapi import FastAPI

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.exc import IntegrityError

from app.config import get_app_config
from auth.routers import auth_router
from auth.utils.exceptions import (
    AuthUserInvalidPasswordException,
    EmailConfirmationExpiredJWTTokenError,
    EmailConfirmationJWTTokenError,
    EmailConfirmationTokenExpiredError,
    EmailConfirmationTokenNotFoundError,
    UserAlreadyActivatedException,
    authjwt_exception_handler,
    email_confirmation_expired_jwt_token_handler,
    email_confirmation_invalid_jwt_token_handler,
    email_confirmation_token_expired_handler,
    email_confirmation_token_not_found_error_handler,
    invalid_auth_credentials_handler,
    user_already_activated_handler,
)
from charity.routers import charities_router
from charity.utils.exceptions import OrganisationHTTPException, organisation_exception_handler
from common.constants.api import ApiConstants
from users.routers import users_router
from users.utils.exceptions import (
    UserNotFoundError,
    UserPermissionError,
    UserPictureExtensionError,
    UserPictureNotFoundError,
    UserPictureResolutionError,
    UserPictureSizeError,
    user_not_found_error_handler,
    user_permission_error_handler,
    user_picture_extension_error_handler,
    user_picture_not_found_error_handler,
    user_picture_resolution_error_handler,
    user_picture_size_error_handler,
)
from utils.exceptions import integrity_error_handler


def create_app(config_name=ApiConstants.DEVELOPMENT_CONFIG.value) -> FastAPI:
    """Application factory function.

    Returns:
    Instance of FastAPI.
    """
    app = FastAPI()
    Config = get_app_config(config_name)
    config = Config()
    app.app_config = config
    # Including routers.
    app_route_includer(app)
    # Adding exceptions handlers.
    app_exception_handler(app)

    @AuthJWT.load_config
    def get_config():
        return config

    return app


def app_route_includer(app: FastAPI) -> FastAPI:
    """Add routers to FastAPI app.

    Args:
        app: FastAPI instance.

    Returns:
    An instance of FastAPI with added routers.
    """
    app.include_router(users_router, prefix=f'/api/v{ApiConstants.API_VERSION_V1.value}')
    app.include_router(auth_router, prefix=f'/api/v{ApiConstants.API_VERSION_V1.value}')
    return app


def app_exception_handler(app: FastAPI) -> FastAPI:
    """Add exception handlers to FastAPI app.

    Args:
        app: FastAPI instance.

    Returns:
    An instance of FastAPI with added exception handlers.
    """
    app.add_exception_handler(AuthJWTException, authjwt_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(AuthUserInvalidPasswordException, invalid_auth_credentials_handler)
    app.add_exception_handler(UserNotFoundError, user_not_found_error_handler)
    app.add_exception_handler(UserPermissionError, user_permission_error_handler)
    app.add_exception_handler(UserPictureSizeError, user_picture_size_error_handler)
    app.add_exception_handler(UserPictureExtensionError, user_picture_extension_error_handler)
    app.add_exception_handler(UserPictureResolutionError, user_picture_resolution_error_handler)
    app.add_exception_handler(UserPictureNotFoundError, user_picture_not_found_error_handler)
    app.add_exception_handler(OrganisationHTTPException, organisation_exception_handler)
    app.add_exception_handler(UserAlreadyActivatedException, user_already_activated_handler)
    app.add_exception_handler(EmailConfirmationTokenNotFoundError, email_confirmation_token_not_found_error_handler)
    app.add_exception_handler(EmailConfirmationTokenExpiredError, email_confirmation_token_expired_handler)
    app.add_exception_handler(EmailConfirmationJWTTokenError, email_confirmation_invalid_jwt_token_handler)
    app.add_exception_handler(EmailConfirmationExpiredJWTTokenError, email_confirmation_expired_jwt_token_handler)
    return app
