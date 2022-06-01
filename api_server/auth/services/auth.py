from datetime import datetime, timedelta
from uuid import UUID
import abc

from fastapi import Depends, status

from fastapi_jwt_auth import AuthJWT
from passlib.hash import argon2
from sqlalchemy.ext.asyncio import AsyncSession

from auth.cruds import ChangePasswordTokenCRUD, EmailConfirmationTokenCRUD
from auth.models import ChangePasswordToken, EmailConfirmationToken
from auth.schemas import (
    AuthUserInputSchema,
    ChangePasswordInputSchema,
    EmailConfirmationTokenInputSchema,
    ForgetPasswordInputSchema,
)
from auth.tasks import send_change_password_letter, send_email_comfirmation_letter
from auth.utils.exceptions import (
    AuthUserInvalidPasswordException,
    ChangePasswordTokenExpiredError,
    ChangePasswordTokenSpamCreationException,
    EmailConfirmationTokenExpiredError,
    EmailConfirmationTokenSpamCreationException,
    ExpiredJWTTokenError,
    UserAlreadyActivatedException,
)
from auth.utils.jwt_tokens import create_jwt_token, create_token_payload, decode_jwt_token
from common.constants.auth import AuthJWTConstants, ChangePasswordTokenConstants, EmailConfirmationTokenConstants
from common.exceptions.auth import (
    AuthExceptionMsgs,
    ChangePasswordTokenExceptionMsgs,
    EmailConfirmationTokenExceptionMsgs,
)
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
        self.change_password_token_crud = ChangePasswordTokenCRUD(session=self.session)

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

    async def get_user_email_confirmation(self, token: str) -> dict:
        """Verifies incoming JWT token and updates User object 'activated_at' field information.

        Args:
            token: JWT token encoded with user's information.

        Returns:
        dict with user's activation success message.
        """
        return await self._get_user_email_confirmation(token)

    async def resend_user_email_confirmation(self, email: EmailConfirmationTokenInputSchema) -> EmailConfirmationToken:
        """Resends email confirmation letter to user's inbox.

        Args:
            email: object validated with EmailConfirmationTokenInputSchema.

        Returns:
        Newly created EmailConfirmationToken object.
        """
        return await self._resend_user_email_confirmation(email)

    async def forgot_password(self, email: ForgetPasswordInputSchema) -> ChangePasswordToken:
        """Creates ChangePasswordToken object and sends email with link to change user's password.

        Args:
            email: object validated with ForgetPasswordInputSchema.

        Returns:
        Newly created ChangePasswordToken object.
        """
        return await self._forgot_password(email)

    async def change_password(self, pass_data: ChangePasswordInputSchema) -> dict:
        """Verifies incoming JWT token and updates User object 'password' field information.

        Args:
            pass_data: JWT token encoded with user's information.

        Returns:
        dict with user's change password success message.
        """
        return await self._change_password(pass_data)

    @classmethod
    async def _login(cls, user: AuthUserInputSchema) -> None:
        pass

    @classmethod
    async def _verify_password(cls, password: str, password_hash: str) -> None:
        pass

    @classmethod
    async def _me(cls) -> None:
        pass

    @classmethod
    async def _logout(cls) -> None:
        pass

    @classmethod
    async def _refresh_token(cls) -> None:
        pass

    @classmethod
    async def _get_user_email_confirmation(cls, token: str) -> None:
        pass

    @classmethod
    async def _resend_user_email_confirmation(cls, email: EmailConfirmationTokenInputSchema) -> None:
        pass

    @classmethod
    async def _forgot_password(cls, email: ForgetPasswordInputSchema) -> None:
        pass

    @classmethod
    async def _change_password(cls, pass_data: ChangePasswordInputSchema) -> None:
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
        await self._validate_email_confirmation_token(email_confirmation_token)
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
        await self._prevent_email_confirmation_token_spam_creation(user.id)
        jwt_token_payload = create_token_payload(
            data=str(user.id),
            time_amount=EmailConfirmationTokenConstants.TOKEN_EXPIRE_7.value,
            time_unit=EmailConfirmationTokenConstants.MINUTES.value,
        )
        jwt_token = create_jwt_token(payload=jwt_token_payload, key=user.password)
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

    async def _validate_email_confirmation_token(self, token: EmailConfirmationToken) -> None:
        """Validates EmailConfirmationToken not to be expired and user's not to be already activated.

        Args:
            token: An EmailConfirmationToken object.

        Returns:
        Nothing.
        """
        await self._validate_token_user_activation(token)
        await self._validate_email_confirmation_token_expiration(token)
        await self._validate_email_confirmation_jwt_token_expiration(token)

    async def _validate_email_confirmation_token_expiration(self, token: EmailConfirmationToken) -> bool:
        """Check if token has 'expired_at' field filled already.

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

    async def _validate_email_confirmation_jwt_token_expiration(self, token: EmailConfirmationToken) -> None:
        """Decodes jwt token and check expiration date set in token.

        Args:
            token: An EmailConfirmationToken object.

        Raise:
            ExpiredJWTTokenError in case JWT token expired.

        Returns:
        Nothing.
        """
        try:
            decode_jwt_token(token=token.token, key=token.user.password)
        except ExpiredJWTTokenError as exc:
            await self.email_confirmation_token_crud._expire_email_confirmation_token_by_id(token.id)
            self._log.debug(exc)
            raise exc

    async def _forgot_password(self, email: ForgetPasswordInputSchema) -> ChangePasswordToken:
        user = await self.user_crud.get_user_by_email(email.email)
        await self._prevent_change_password_token_spam_creation(user.id)
        jwt_token_payload = create_token_payload(
            data=str(user.id),
            time_amount=ChangePasswordTokenConstants.TOKEN_EXPIRE_1.value,
            time_unit=EmailConfirmationTokenConstants.DAYS.value,
        )
        jwt_token = create_jwt_token(payload=jwt_token_payload, key=user.password)
        db_change_password_token = await self.change_password_token_crud.add_change_password_token(
            id_=user.id,
            token=jwt_token,
        )
        send_change_password_letter.apply_async(
            kwargs={
                'token': db_change_password_token,
            },
            serializers='pickle',
        )
        return db_change_password_token

    async def _prevent_change_password_token_spam_creation(self, user_id: UUID) -> None:
        """Checks user's change password token 'created_at' value against min token lifetime to prevent endpoint abuse.

        Args:
            user_id: UUID of a user.

        Raise:
            ChangePasswordTokenSpamCreationException in case of new token trying to be created too soon.

        Returns:
        Nothing.
        """
        token = await self.change_password_token_crud._get_last_non_expired_change_password_token_by_user_id(user_id)
        if token:
            MINUMUM_TOKEN_LIFETIME = timedelta(**ChangePasswordTokenConstants.MIN_TOKEN_LIFETIME_TIMEDELTA.value)
            token_fresh = await self.check_token_freshness(token.created_at, MINUMUM_TOKEN_LIFETIME)
            if token_fresh:
                raise ChangePasswordTokenSpamCreationException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ChangePasswordTokenExceptionMsgs.TOKEN_CREATION_SPAM.value.format(
                        time_amount=ChangePasswordTokenConstants.MIN_TOKEN_LIFETIME.value,
                        time_units=ChangePasswordTokenConstants.MINUTES.value,
                    ),
                )

    async def check_token_freshness(self, token_date: datetime, token_time_limit: timedelta) -> bool:
        """Checks token fressness by comparing creation datetime with specified time limit.

        Args:
            token_date: Token creation datetime.
            token_time_limit: timedelta with token time limit.

        Returns:
        bool of comparison how much time passed from token creation and time limit.
        """
        token_lifetime = datetime.utcnow() - token_date
        return token_lifetime <= token_time_limit

    async def _prevent_email_confirmation_token_spam_creation(self, user_id: UUID) -> None:
        """Checks user's email confirmation token 'created_at' value against min token lifetime to prevent endpoint
        abuse.

        Args:
            user_id: UUID of a user.

        Raise:
            ChangePasswordTokenSpamCreationException in case of new token trying to be created too soon.

        Returns:
        Nothing.
        """
        token = await self.email_confirmation_token_crud._get_last_non_expired_email_confirmation_token_by_user_id(
            user_id,
        )
        if token:
            MINUMUM_TOKEN_LIFETIME = timedelta(**EmailConfirmationTokenConstants.MIN_TOKEN_LIFETIME_TIMEDELTA.value)
            token_fresh = await self.check_token_freshness(token.created_at, MINUMUM_TOKEN_LIFETIME)
            if token_fresh:
                raise EmailConfirmationTokenSpamCreationException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=EmailConfirmationTokenExceptionMsgs.TOKEN_CREATION_SPAM.value.format(
                        time_amount=EmailConfirmationTokenConstants.MIN_TOKEN_LIFETIME.value,
                        time_units=EmailConfirmationTokenConstants.MINUTES.value,
                    ),
                )

    async def _change_password(self, pass_data: ChangePasswordInputSchema) -> dict:
        db_token = await self.change_password_token_crud._get_change_password_by_token(pass_data.token)
        await self._validate_change_password_token(db_token)
        await self.change_password_token_crud._expire_change_password_token_by_id(db_token.id)
        password_hash = await self.user_crud._hash_password(pass_data.password)
        await self.user_crud._update_user_password(id_=db_token.user.id, pass_hash=password_hash)
        ChangePasswordTokenConstants.SUCCESSFUL_CHANGE_PASSWORD_MSG.value['message'] = (
            ChangePasswordTokenConstants.SUCCESSFUL_CHANGE_PASSWORD_MSG.value['message'].format(
                email=db_token.user.email,
            )
        )
        return ChangePasswordTokenConstants.SUCCESSFUL_CHANGE_PASSWORD_MSG.value

    async def _validate_change_password_token(self, token: ChangePasswordToken) -> None:
        """Validates ChangePasswordToken not to be expired in db and inside JWT token payload.

        Args:
            token: An EmailConfirmationToken object.

        Returns:
        Nothing.
        """
        await self._validate_change_password_token_expiration(token)
        await self._validate_change_password_jwt_token_expiration(token)

    async def _validate_change_password_token_expiration(self, token: ChangePasswordToken) -> bool:
        """Check if token has 'expired_at' field filled already.

        Args:
            token: An ChangePasswordToken object.

        Raise:
            ChangePasswordTokenExpiredError if 'token.expired_at' field filled with data.

        Returns:
        bool of content 'token.expired_at' field.
        """
        if token.expired_at:
            raise ChangePasswordTokenExpiredError(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ChangePasswordTokenExceptionMsgs.TOKEN_EXPIRED.value,
            )
        return bool(token.expired_at)

    async def _validate_change_password_jwt_token_expiration(self, token: ChangePasswordToken) -> None:
        """Decodes jwt token and check expiration date set in token.

        Args:
            token: An ChangePasswordToken object.

        Raise:
            ExpiredJWTTokenError in case JWT token expired.

        Returns:
        Nothing.
        """
        try:
            decode_jwt_token(token=token.token, key=token.user.password)
        except ExpiredJWTTokenError as exc:
            await self.change_password_token_crud._expire_change_password_token_by_id(token.id)
            self._log.debug(exc)
            raise exc
