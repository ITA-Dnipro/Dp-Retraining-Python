from fastapi import APIRouter, Depends

from auth.schemas import AuthUserInputSchema, AuthUserOutputSchema, AuthUserLogoutSchema
from auth.services import AuthService
from users.schemas import UserOutputSchema

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post('/login', response_model=AuthUserOutputSchema)
async def login(user: AuthUserInputSchema, auth_service: AuthService = Depends()):
    """POST '/login' endpoint func, return auth header."""
    return await auth_service.login(user)


@auth_router.get('/me', response_model=UserOutputSchema)
async def auth_me(auth_service: AuthService = Depends()):
    """GET '/me' endpoint provides information about currently authenticated user."""
    return await auth_service.me()


@auth_router.post('/logout', response_model=AuthUserLogoutSchema)
async def logout(auth_service: AuthService = Depends()):
    """POST '/logout' endpoint logging out currently authenticated user."""
    return await auth_service.logout()


@auth_router.post('/refresh', response_model=AuthUserOutputSchema)
async def refresh(auth_service: AuthService = Depends()):
    """POST '/refresh' endpoint refreshing user's access and refresh tokens."""
    return await auth_service.refresh_token()
