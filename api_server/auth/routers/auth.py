from fastapi import APIRouter, Depends, status

from auth.schemas import (
    AuthUserInputSchema,
    AuthUserLogoutSchema,
    AuthUserOutputSchema,
    ChangePasswordInputSchema,
    ChangePasswordOutputSchema,
    EmailConfirmationTokenInputSchema,
    EmailConfirmationTokenOutputSchema,
    EmailConfirmationTokenSuccessSchema,
    ForgetPasswordInputSchema,
    ForgetPasswordOutputSchema,
)
from auth.services import AuthService
from common.schemas.responses import ResponseBaseSchema
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


@auth_router.get('/email-confirmation', response_model=ResponseBaseSchema)
async def get_user_email_confiramation(token: str, auth_service: AuthService = Depends()) -> ResponseBaseSchema:
    """GET '/auth/email-confirmation' endpoint view function.

    Args:
        token: query parameter with JWT token.
        auth_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with EmailConfirmationTokenSuccessSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=EmailConfirmationTokenSuccessSchema(**await auth_service.get_user_email_confirmation(token=token)),
        errors=[],
    )


@auth_router.post('/email-confirmation', response_model=ResponseBaseSchema, status_code=status.HTTP_201_CREATED)
async def post_user_email_confirmation(
        email: EmailConfirmationTokenInputSchema, auth_service: AuthService = Depends(),
) -> ResponseBaseSchema:
    """POST '/auth/email-confirmation' endpoint view function.

    Args:
        email: object validated with EmailConfirmationTokenInputSchema.
        auth_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with EmailConfirmationTokenOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_201_CREATED,
        data=EmailConfirmationTokenOutputSchema.from_orm(await auth_service.resend_user_email_confirmation(email)),
        errors=[],
    )


@auth_router.post('/forgot-password', response_model=ResponseBaseSchema, status_code=status.HTTP_201_CREATED)
async def post_forgot_password(
        email: ForgetPasswordInputSchema, auth_service: AuthService = Depends(),
) -> ResponseBaseSchema:
    """POST '/auth/forgot-password' endpoint view function.

    Args:
        email: object validated with ForgetPasswordInputSchema.
        auth_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with ForgetPasswordOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_201_CREATED,
        data=ForgetPasswordOutputSchema.from_orm(await auth_service.forgot_password(email)),
        errors=[],
    )


@auth_router.post('/change-password', response_model=ResponseBaseSchema)
async def post_change_password(
        pass_data: ChangePasswordInputSchema, auth_service: AuthService = Depends(),
) -> ResponseBaseSchema:
    """POST '/auth/change-password' endpoint view function.

    Args:
        pass_data: object validated with ChangePasswordInputSchema.
        auth_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with ChangePasswordOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_201_CREATED,
        data=ChangePasswordOutputSchema(**await auth_service.change_password(pass_data)),
        errors=[],
    )
