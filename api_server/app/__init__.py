from fastapi import FastAPI

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from app.config import Settings
from auth.routers import auth_router
from auth.utils.exceptions import authjwt_exception_handler
from common.constants.api import ApiConstants
from users.routers import users_router


def create_app() -> FastAPI:
    """Application factory function.

    Returns:
    Instance of FastAPI.
    """
    app = FastAPI()

    app.include_router(users_router, prefix=f'/api/v{ApiConstants.API_VERSION_V1.value}')
    app.include_router(auth_router, prefix=f'/api/v{ApiConstants.API_VERSION_V1.value}')

    app.add_exception_handler(AuthJWTException, authjwt_exception_handler)

    @AuthJWT.load_config
    def get_config():
        return Settings()

    return app
