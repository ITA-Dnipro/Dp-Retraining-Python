from functools import partial
import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.exc import IntegrityError

from app.config import get_app_config
from auth.routers import auth_router
from auth.utils.exceptions import (
    AuthUserInvalidPasswordException,
    ChangePasswordTokenExpiredError,
    ChangePasswordTokenNotFoundError,
    ChangePasswordTokenSpamCreationException,
    EmailConfirmationTokenExpiredError,
    EmailConfirmationTokenNotFoundError,
    EmailConfirmationTokenSpamCreationException,
    ExpiredJWTTokenError,
    JWTTokenError,
    UserAlreadyActivatedException,
    authjwt_exception_handler,
    change_password_token_anti_creation_spam_handler,
    change_password_token_expired_in_db_handler,
    change_password_token_not_found_handler,
    email_confirmation_token_anti_creation_spam_handler,
    email_confirmation_token_expired_handler,
    email_confirmation_token_not_found_error_handler,
    expired_jwt_token_handler,
    invalid_auth_credentials_handler,
    invalid_jwt_token_handler,
    user_already_activated_handler,
)
from charities.routers import charities_router
from charities.utils.exceptions import (
    CharityEmployeeDuplicateError,
    CharityEmployeePermissionError,
    CharityEmployeeRoleDuplicateError,
    CharityEmployeeRolePermissionError,
    CharityNotFoundError,
    EmployeeRoleNotSupportedError,
    charity_employee_permission_error_handler,
    charity_employee_role_permission_error_handler,
    charity_not_found_error_handler,
    employee_already_added_to_charity_error_handler,
    employee_role_already_added_to_employee_error_handler,
    employee_role_not_supported_error_handler,
)
from common.constants.api import ApiConstants
from fundraisers.routers import fundraisers_router
from fundraisers.utils.exceptions import (
    FundraiseNotFoundError,
    FundraisePermissionError,
    fundraise_no_permissions_error_handler,
    fundraise_not_found_error_handler,
)
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
from utils.prepopulates.employee_roles import populate_employee_roles_table
from utils.prepopulates.fundraise_statuses import populate_fundraise_statuses_table

load_dotenv()


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
    # Allow CORS
    allowed_origins: list = json.loads(os.getenv('API_SERVER_ALLOWED_ORIGINS'))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Adding on start_up events.
    app_on_start_up_events(app)

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
    app.include_router(charities_router, prefix=f'/api/v{ApiConstants.API_VERSION_V1.value}')
    app.include_router(fundraisers_router, prefix=f'/api/v{ApiConstants.API_VERSION_V1.value}')
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
    app.add_exception_handler(CharityNotFoundError, charity_not_found_error_handler)
    app.add_exception_handler(UserAlreadyActivatedException, user_already_activated_handler)
    app.add_exception_handler(EmailConfirmationTokenNotFoundError, email_confirmation_token_not_found_error_handler)
    app.add_exception_handler(EmailConfirmationTokenExpiredError, email_confirmation_token_expired_handler)
    app.add_exception_handler(JWTTokenError, invalid_jwt_token_handler)
    app.add_exception_handler(ExpiredJWTTokenError, expired_jwt_token_handler)
    app.add_exception_handler(
        ChangePasswordTokenSpamCreationException, change_password_token_anti_creation_spam_handler,
    )
    app.add_exception_handler(
        EmailConfirmationTokenSpamCreationException, email_confirmation_token_anti_creation_spam_handler,
    )
    app.add_exception_handler(ChangePasswordTokenNotFoundError, change_password_token_not_found_handler)
    app.add_exception_handler(ChangePasswordTokenExpiredError, change_password_token_expired_in_db_handler)
    app.add_exception_handler(FundraiseNotFoundError, fundraise_not_found_error_handler)
    app.add_exception_handler(FundraisePermissionError, fundraise_no_permissions_error_handler)
    app.add_exception_handler(CharityEmployeePermissionError, charity_employee_permission_error_handler)
    app.add_exception_handler(CharityEmployeeRolePermissionError, charity_employee_role_permission_error_handler)
    app.add_exception_handler(CharityEmployeeDuplicateError, employee_already_added_to_charity_error_handler)
    app.add_exception_handler(EmployeeRoleNotSupportedError, employee_role_not_supported_error_handler)
    app.add_exception_handler(CharityEmployeeRoleDuplicateError, employee_role_already_added_to_employee_error_handler)
    return app


def app_on_start_up_events(app: FastAPI) -> FastAPI:
    """Add on start_up handlers to FastAPI app.

    Args:
        app: FastAPI instance.

    Returns:
    An instance of FastAPI with added start_up handlers.
    """
    app.add_event_handler(event_type='startup', func=partial(populate_fundraise_statuses_table, config=app.app_config))
    app.add_event_handler(event_type='startup', func=partial(populate_employee_roles_table, config=app.app_config))
