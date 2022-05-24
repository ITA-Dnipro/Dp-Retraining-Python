from datetime import datetime
from uuid import UUID
import abc

from fastapi import status

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from auth.models import EmailConfirmationToken
from auth.utils.exceptions import EmailConfirmationTokenNotFoundError
from users.cruds.users_crud import UserCRUD
from utils.logging import setup_logging


class AbstractEmailConfirmationTokenCRUD(metaclass=abc.ABCMeta):

    def __init__(self, session) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def add_email_confirmation_token(self, id_: UUID, token: str) -> EmailConfirmationToken:
        """Add EmailConfirmationToken object to the database.

        Args:
            id_: UUID of User object.
            token: string with encoded JWT token.

        Returns:
        newly created EmailConfirmationToken object.
        """
        return await self._add_email_confirmation_token(id_, token)

    async def get_email_confirmation_by_token(self, token: str) -> EmailConfirmationToken:
        """Get EmailConfirmationToken object from database filtered by token field.

        Args:
            token: JWT token stored in EmailConfirmationToken token field.

        Returns:
        Single EmailConfirmationToken object filtered by token field.
        """
        return await self._get_email_confirmation_by_token(token)

    @abc.abstractclassmethod
    async def _add_email_confirmation_token(self, id_: UUID, token: str) -> None:
        pass

    @abc.abstractclassmethod
    async def _get_email_confirmation_by_token(self, token: str) -> None:
        pass


class EmailConfirmationTokenCRUD(AbstractEmailConfirmationTokenCRUD, UserCRUD):

    async def _add_email_confirmation_token(self, id_: UUID, token: str) -> EmailConfirmationToken:
        user = await self.get_user_by_id(id_=id_)
        await self._expire_all_existing_email_confirmation_tokens(id_=id_)
        email_confirmation_token = EmailConfirmationToken(user_id=user.id, token=token)
        self.session.add(email_confirmation_token)
        await self.session.commit()
        await self.session.refresh(email_confirmation_token)
        return email_confirmation_token

    async def _expire_all_existing_email_confirmation_tokens(self, id_: UUID) -> None:
        """Finds all user's non expired tokens and expires them by setting 'expired_at' field with current time.

        Args:
            id_: UUID of a user.

        Returns:
        Nothing.
        """
        await self.session.execute(
            update(
                EmailConfirmationToken
            ).where(
                EmailConfirmationToken.user_id == id_
            ).where(
                EmailConfirmationToken.expired_at == None # noqa
            ).values(
                expired_at=datetime.utcnow()
            )
        )
        await self.session.commit()

    async def _expire_email_confirmation_token_by_id(self, id_: UUID) -> None:
        """Expires specific EmailConfirmationToken object by setting 'expired_at' field with current time.

        Args:
            id_: UUID of EmailConfirmationToken object.

        Returns:
        Nothing.
        """
        await self.session.execute(
            update(
                EmailConfirmationToken
            ).where(
                EmailConfirmationToken.id == id_
            ).values(
                expired_at=datetime.utcnow()
            )
        )
        await self.session.commit()

    async def _email_confirmation_token_exists(self, column: str, value: UUID | str) -> bool:
        email_confirmation_token = await self.session.execute(
            select(EmailConfirmationToken).where(EmailConfirmationToken.__table__.columns[column] == value),
        )
        try:
            email_confirmation_token.one()
        except NoResultFound as err:
            err_msg = f"EmailConfirmationToken with {column}: '{value}' not found."
            self._log.debug(err_msg)
            self._log.debug(err)
            raise EmailConfirmationTokenNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return True

    async def _select_email_confirmation_token(self, column: str, value: UUID | str) -> EmailConfirmationToken:
        email_confirmation_token_exists = await self._email_confirmation_token_exists(column=column, value=value)
        if email_confirmation_token_exists:
            email_confirmation_token = await self.session.execute(
                select(EmailConfirmationToken).where(EmailConfirmationToken.__table__.columns[column] == value),
            )
            return email_confirmation_token.scalar_one()

    async def _get_email_confirmation_by_token(self, token: str) -> EmailConfirmationToken:
        return await self._select_email_confirmation_token(column='token', value=token)
