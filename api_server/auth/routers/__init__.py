from auth.schemas import (AuthUserInputSchema, AuthUserLogoutSchema,
                          AuthUserOutputSchema)
from auth.services import AuthService
from common.schemas.responses import ResponseBaseSchema
from fastapi import APIRouter, Depends, status
from users.schemas import UserOutputSchema

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post('/login', response_model=ResponseBaseSchema)
async def login(user: AuthUserInputSchema, auth_service: AuthService = Depends()) -> ResponseBaseSchema:
    """POST '/auth/login' endpoint view function.

    Args:
        user: object validated with AuthUserInputSchema.
        auth_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with AuthUserOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=AuthUserOutputSchema(**await auth_service.login(user)),
        errors=[],
    )


@auth_router.get('/me', response_model=ResponseBaseSchema)
async def auth_me(auth_service: AuthService = Depends()) -> ResponseBaseSchema:
    """GET '/auth/me' endpoint view function.

    Args:
        auth_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with UserOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=UserOutputSchema.from_orm(await auth_service.me()),
        errors=[],
    )


@auth_router.post('/logout', response_model=ResponseBaseSchema)
async def logout(auth_service: AuthService = Depends()) -> ResponseBaseSchema:
    """POST '/auth/logout' endpoint view function.

    Args:
        auth_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with AuthUserLogoutSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=AuthUserLogoutSchema(**await auth_service.logout()),
        errors=[],
    )


@auth_router.post('/refresh', response_model=ResponseBaseSchema)
async def refresh(auth_service: AuthService = Depends()) -> ResponseBaseSchema:
    """POST '/auth/refresh' endpoint view function.

    Args:
        auth_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with AuthUserOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=AuthUserOutputSchema(**await auth_service.refresh_token()),
        errors=[],
    )
