from datetime import timedelta
import abc

from fastapi import Depends, status

from fastapi_jwt_auth import AuthJWT
from passlib.hash import argon2
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import AuthUserInputSchema
from auth.utils.exceptions import AuthUserInvalidPasswordException
from common.constants.auth import AuthJWTConstants
from common.exceptions.auth import AuthExceptionMsgs
from db import get_session
from users.cruds import UserCRUD
from users.models import User
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
        self.user_crud = UserCRUD(session=self.session)
        self.Authorize = Authorize

    async def login(self, user: AuthUserInputSchema) -> dict:
        """Creates JTW access and refresh tokens based on user credentials.

        Args:
            user: Serialized AuthUserInputSchema object.

        Returns:
        dict with created access and refresh tokens.
        """
        return await self._login(user)

    async def me(self) -> User:
        """Gets user information based on JWT credentials.

        Returns:
        User object from db.
        """
        return await self._me()

    async def logout(self) -> dict:
        """Unset JWT credentials for currently authenticated user.

        Returns:
        dict with response message.
        """
        return await self._logout()

    async def verify_password(self, password: str, password_hash: str) -> bool:
        """Checks password and password hash with argon2 algorithm.

        Args:
            password: string with password.
            password_hash: string with password hash.

        Returns:
        bool of verifying password with argon2 algorithm.
        """
        return await self._verify_password(password, password_hash)

    async def refresh_token(self) -> dict:
        """Creates JTW access and refresh tokens based on user credentials.

        Returns:
        dict with newly created access and refresh tokens.
        """
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
        db_user = await self.user_crud.get_user_by_username(username=user.username)
        if await self.verify_password(password=user.password, password_hash=db_user.password):
            user_claims = {
                'user_data': {
                    'id': str(db_user.id),
                    'email': db_user.email,
                    'phone': db_user.phone_number,
                },
            }
            access_token = await self._create_jwt_token(
                subject=user.username,
                token_type=AuthJWTConstants.ACCESS_TOKEN_NAME.value,
                time_unit=AuthJWTConstants.MINUTES.value,
                time_amount=AuthJWTConstants.TOKEN_EXPIRE_60.value,
                user_claims=user_claims,
            )
            refresh_token = await self._create_jwt_token(
                subject=user.username,
                token_type=AuthJWTConstants.REFRESH_TOKEN_NAME.value,
                time_unit=AuthJWTConstants.DAYS.value,
                time_amount=AuthJWTConstants.TOKEN_EXPIRE_7.value,
                user_claims=user_claims,
            )

            self.Authorize.set_access_cookies(access_token)
            self.Authorize.set_refresh_cookies(refresh_token)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        raise AuthUserInvalidPasswordException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=AuthExceptionMsgs.WRONG_USERNAME_OR_PASSWORD.value,
            )

    async def _create_jwt_token(
            self, subject: str, token_type: str, time_amount: int, time_unit: str, user_claims: dict,
    ) -> str:
        """Creates JWT access or refresh tokens.

        Args:
            subject: string to create token.
            token_type: string with token_type.
            time_amount: token lifetime amount.
            time_unit: token lifetime unit.
            user_claims: additional user information.

        Returns:
        Return access or refresh token with set parameters.
        """
        CREATE_TOKEN_METHODS = {
            'access': self.Authorize.create_access_token,
            'refresh': self.Authorize.create_refresh_token,
        }
        expires_time = timedelta(**{time_unit: time_amount})
        return CREATE_TOKEN_METHODS[token_type](subject=subject, expires_time=expires_time, user_claims=user_claims)

    async def _me(self) -> None:
        self.Authorize.jwt_required()
        current_user = self.Authorize.get_jwt_subject()
        user = await self.user_crud.get_user_by_username(current_user)
        return user

    async def _logout(self) -> None:
        self.Authorize.jwt_required()
        self.Authorize.unset_jwt_cookies()
        return {'message': AuthJWTConstants.LOGOUT_MSG.value}

    async def _refresh_token(self) -> None:
        self.Authorize.jwt_refresh_token_required()
        current_user = self.Authorize.get_jwt_subject()
        current_user_claims = {'user_data': self.Authorize.get_raw_jwt()['user_data']}
        access_token = await self._create_jwt_token(
            subject=current_user,
            token_type=AuthJWTConstants.ACCESS_TOKEN_NAME.value,
            time_unit=AuthJWTConstants.MINUTES.value,
            time_amount=AuthJWTConstants.TOKEN_EXPIRE_60.value,
            user_claims=current_user_claims,
        )
        refresh_token = await self._create_jwt_token(
            subject=current_user,
            token_type=AuthJWTConstants.REFRESH_TOKEN_NAME.value,
            time_unit=AuthJWTConstants.DAYS.value,
            time_amount=AuthJWTConstants.TOKEN_EXPIRE_7.value,
            user_claims=current_user_claims,
        )
        self.Authorize.set_access_cookies(access_token)
        self.Authorize.set_refresh_cookies(refresh_token)
        return {'access_token': access_token, 'refresh_token': refresh_token}
