from datetime import timedelta
import abc

from fastapi import Depends, status

from fastapi_jwt_auth import AuthJWT
from passlib.hash import argon2
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import AuthUserInputSchema
from auth.utils.exceptions import AuthUserInvalidPasswordException
from common.constants.auth import AuthJWTConstants
from db import get_session
from users.services import UserService
from utils.logging import setup_logging


class AbstractAuthService(metaclass=abc.ABCMeta):

    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        Authorize: AuthJWT = Depends(),
    ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.user_service = UserService(session=self.session)
        self.Authorize = Authorize

    async def login(self, user: AuthUserInputSchema) -> None:
        """Login user with credentials."""
        return await self._login(user)

    async def me(self) -> None:
        """Return currently authenticated user."""
        return await self._me()

    async def logout(self) -> None:
        """Unset credentials for currently authenticated user."""
        return await self._logout()

    async def verify_password(self, password: str, password_hash: str) -> bool:
        """Return bool of verifying password with argon2 algorithm."""
        return await self._verify_password(password, password_hash)

    async def refresh_token(self) -> None:
        """Refresh and return access and refresh tokens."""
        return await self._refresh_token()

    @abc.abstractclassmethod
    async def _login(user: AuthUserInputSchema) -> None:
        pass

    @abc.abstractclassmethod
    async def _verify_password(self, password: str, password_hash: str) -> None:
        pass

    @abc.abstractclassmethod
    async def _me(self) -> None:
        pass

    @abc.abstractclassmethod
    async def _logout(self) -> None:
        pass

    @abc.abstractclassmethod
    async def _refresh_token(self) -> None:
        pass


class AuthService(AbstractAuthService):

    async def _verify_password(self, password: str, password_hash: str) -> bool:
        return argon2.verify(password, password_hash)

    async def _login(self, user: AuthUserInputSchema) -> None:
        db_user = await self.user_service.get_user_by_username(username=user.username)
        if await self.verify_password(password=user.password, password_hash=db_user.password):
            access_token = await self._create_jwt_token(
                subject=user.username,
                token_type=AuthJWTConstants.ACCESS_TOKEN_NAME.value,
                time_unit=AuthJWTConstants.MINUTES.value,
                time_amount=AuthJWTConstants.TOKEN_EXPIRE_60.value,
            )
            refresh_token = await self._create_jwt_token(
                subject=user.username,
                token_type=AuthJWTConstants.REFRESH_TOKEN_NAME.value,
                time_unit=AuthJWTConstants.DAYS.value,
                time_amount=AuthJWTConstants.TOKEN_EXPIRE_7.value,

            )

            self.Authorize.set_access_cookies(access_token)
            self.Authorize.set_refresh_cookies(refresh_token)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        raise AuthUserInvalidPasswordException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorect username or password.',
            )

    async def _create_jwt_token(self, subject: str, token_type: str, time_amount: int, time_unit: str) -> str:
        """Return access or refresh token with set parameters."""
        CREATE_TOKEN_METHODS = {
            'access': self.Authorize.create_access_token,
            'refresh': self.Authorize.create_refresh_token,
        }
        expires_time = timedelta(**{time_unit: time_amount})
        return CREATE_TOKEN_METHODS[token_type](subject=subject, expires_time=expires_time)

    async def _me(self) -> None:
        self.Authorize.jwt_required()
        current_user = self.Authorize.get_jwt_subject()
        user = await self.user_service.get_user_by_username(current_user)
        return user

    async def _logout(self) -> None:
        self.Authorize.jwt_required()
        self.Authorize.unset_jwt_cookies()
        return {'message': 'Successfully logout.'}

    async def _refresh_token(self) -> None:
        self.Authorize.jwt_refresh_token_required()
        current_user = self.Authorize.get_jwt_subject()
        access_token = await self._create_jwt_token(
            subject=current_user,
            token_type=AuthJWTConstants.ACCESS_TOKEN_NAME.value,
            time_unit=AuthJWTConstants.MINUTES.value,
            time_amount=AuthJWTConstants.TOKEN_EXPIRE_60.value,
        )
        refresh_token = await self._create_jwt_token(
            subject=current_user,
            token_type=AuthJWTConstants.REFRESH_TOKEN_NAME.value,
            time_unit=AuthJWTConstants.DAYS.value,
            time_amount=AuthJWTConstants.TOKEN_EXPIRE_7.value,
        )
        self.Authorize.set_access_cookies(access_token)
        self.Authorize.set_refresh_cookies(refresh_token)
        return {'access_token': access_token, 'refresh_token': refresh_token}
