from datetime import timedelta
import abc

from fastapi import Depends, status

from fastapi_jwt_auth import AuthJWT
from passlib.hash import argon2
from sqlalchemy.ext.asyncio import AsyncSession

from auth.cruds import EmailConfirmationTokenCRUD
from auth.models import EmailConfirmationToken
from auth.schemas import AuthUserInputSchema, EmailConfirmationTokenInputSchema
from auth.tasks import send_email_comfirmation_letter
from auth.utils.email_confirmation_tokens import create_email_cofirmation_token, decode_jwt_token
from auth.utils.exceptions import (
    AuthUserInvalidPasswordException,
    EmailConfirmationExpiredJWTTokenError,
    EmailConfirmationTokenExpiredError,
    UserAlreadyActivatedException,
)
from common.constants.auth import AuthJWTConstants, EmailConfirmationTokenConstants
from common.exceptions.auth import AuthExceptionMsgs, EmailConfirmationTokenExceptionMsgs
from db import get_session
from users.cruds import UserCRUD
from users.models import User
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
        self.email_confirmation_token_crud = EmailConfirmationTokenCRUD(session=self.session)

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

    async def get_user_email_confirmation(self, token: str) -> User:
        """Verifies incoming JWT token and updates User object 'activated_at' field information.

        Args:
            token: JWT token encoded with user's information.

        Returns:
        User object.
        """
        return await self._get_user_email_confirmation(token)

    async def resend_user_email_confirmation(self, email: EmailConfirmationTokenInputSchema) -> None:
        """Resends email confirmation letter to user's inbox.

        Args:
            email: object validated with EmailConfirmationTokenInputSchema.

        Returns:
        Nothing.
        """
        return await self._resend_user_email_confirmation(email)

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

    @abc.abstractclassmethod
    async def _get_user_email_confirmation(self, token: str) -> None:
        pass

    @abc.abstractclassmethod
    async def _resend_user_email_confirmation(self, email: EmailConfirmationTokenInputSchema) -> None:
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

    async def _get_user_email_confirmation(self, token: str):
        email_confirmation_token = await self.email_confirmation_token_crud.get_email_confirmation_by_token(token)
        await self._validate_token(email_confirmation_token)
        await self.email_confirmation_token_crud._expire_email_confirmation_token_by_id(email_confirmation_token.id)
        await self.email_confirmation_token_crud._activate_user_by_id(email_confirmation_token.user.id)
        EmailConfirmationTokenConstants.SUCCESSFUL_EMAIL_CONFIRMATION_MSG.value['message'] = (
            EmailConfirmationTokenConstants.SUCCESSFUL_EMAIL_CONFIRMATION_MSG.value['message'].format(
                email=email_confirmation_token.user.email,
            )
        )
        return EmailConfirmationTokenConstants.SUCCESSFUL_EMAIL_CONFIRMATION_MSG.value

    async def _resend_user_email_confirmation(self, email: EmailConfirmationTokenInputSchema) -> EmailConfirmationToken:
        user = await self.user_crud.get_user_by_email(email.email)
        await self._check_user_is_activated(user)
        jwt_token = create_email_cofirmation_token(user)
        db_email_confirmation_token = await self.email_confirmation_token_crud.add_email_confirmation_token(
            id_=user.id,
            token=jwt_token,
        )
        send_email_comfirmation_letter.apply_async(
            kwargs={
                'email_confirmation_token': db_email_confirmation_token,
            },
            serializers='pickle',
        )
        return db_email_confirmation_token

    async def _check_user_is_activated(self, user: User) -> bool:
        """Checks if user object has 'activated_at' field filled with data.

        Args:
            user: User object.

        Raise:
            UserAlreadyActivatedException if 'user.activated_at' field filled with data.

        Returns:
        bool of content 'user.activated_at' field.
        """
        if user.activated_at:
            raise UserAlreadyActivatedException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=EmailConfirmationTokenExceptionMsgs.USER_ALREADY_ACTIVATED.value.format(user_email=user.email),
            )
        return bool(user.activated_at)

    async def _validate_token(self, token: EmailConfirmationToken) -> None:
        """Validates EmailConfirmationToken not to be expired and user's not to be already activated.

        Args:
            token: An EmailConfirmationToken object.

        Returns:
        Nothing.
        """
        await self._validate_token_user_activation(token)
        await self._validate_db_token_expiration(token)
        await self._validate_jwt_token_expiration(token)

    async def _validate_db_token_expiration(self, token: EmailConfirmationToken) -> bool:
        """Check if token has expired_at filled aleready.

        Args:
            token: An EmailConfirmationToken object.

        Raise:
            EmailConfirmationTokenExpiredError if 'token.expired_at' field filled with data.

        Returns:
        bool of content 'token.expired_at' field.
        """
        if token.expired_at:
            raise EmailConfirmationTokenExpiredError(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=EmailConfirmationTokenExceptionMsgs.TOKEN_EXPIRED.value,
            )
        return bool(token.expired_at)

    async def _validate_token_user_activation(self, token: EmailConfirmationToken) -> None:
        """Check if user already activated and expires current user's token.

        Args:
            token: An EmailConfirmationToken object.

        Raise:
            UserAlreadyActivatedException if 'user.activated_at' field filled with data.

        Returns:
        Nothing.
        """
        try:
            await self._check_user_is_activated(token.user)
        except UserAlreadyActivatedException as exc:
            await self.email_confirmation_token_crud._expire_email_confirmation_token_by_id(token.id)
            self._log.debug(exc)
            raise exc

    async def _validate_jwt_token_expiration(self, token: EmailConfirmationToken) -> None:
        """Decodes jwt token and check expiration date set in token.

        Args:
            token: An EmailConfirmationToken object.

        Returns:
        Nothing.
        """
        try:
            decode_jwt_token(token=token.token, key=token.user.password)
        except EmailConfirmationExpiredJWTTokenError as exc:
            await self.email_confirmation_token_crud._expire_email_confirmation_token_by_id(token.id)
            self._log.debug(exc)
            raise exc
