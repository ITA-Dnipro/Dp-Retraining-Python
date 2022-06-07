from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, select, update

from auth.models import EmailConfirmationToken
from users.cruds.users_crud import UserCRUD
from utils.logging import setup_logging


class EmailConfirmationTokenCRUD(UserCRUD):

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

    async def _add_email_confirmation_token(self, id_: UUID, token: str) -> EmailConfirmationToken:
        await self._expire_all_existing_email_confirmation_tokens(id_=id_)
        email_confirmation_token = EmailConfirmationToken(user_id=id_, token=token)
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
        q = update(
            EmailConfirmationToken
        ).where(
            and_(
                EmailConfirmationToken.user_id == id_,
                EmailConfirmationToken.expired_at == None, # noqa
            )
        ).values(
            expired_at=datetime.utcnow()
        )
        await self.session.execute(q)
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

    async def _select_email_confirmation_token(self, column: str, value: UUID | str) -> EmailConfirmationToken:
        self._log.debug(f'Getting EmailConfirmationToken with: "{column}": "{value}" from the db.')
        email_confirmation_token = await self.session.execute(
            select(EmailConfirmationToken).where(EmailConfirmationToken.__table__.columns[column] == value),
        )
        return email_confirmation_token.scalars().one_or_none()

    async def get_email_confirmation_by_token(self, token: str) -> EmailConfirmationToken:
        """Get EmailConfirmationToken object from database filtered by token field.

        Args:
            token: JWT token stored in EmailConfirmationToken token field.

        Returns:
        Single EmailConfirmationToken object filtered by token field.
        """
        return await self._get_email_confirmation_by_token(token)

    async def get_email_confirmation_by_token(self, token: str) -> EmailConfirmationToken:
        """Get EmailConfirmationToken object from database filtered by token field.

        Args:
            token: JWT token stored in EmailConfirmationToken token field.

        Returns:
        Single EmailConfirmationToken object filtered by token field.
        """
        return await self._get_email_confirmation_by_token(token)

    async def _get_email_confirmation_by_token(self, token: str) -> EmailConfirmationToken:
        return await self._select_email_confirmation_token(column='token', value=token)

    async def _get_last_non_expired_email_confirmation_token_by_user_id(self, user_id: UUID) -> EmailConfirmationToken:
        q = select(
            EmailConfirmationToken
        ).where(
            and_(
                EmailConfirmationToken.user_id == user_id,
                EmailConfirmationToken.expired_at == None,  # noqa
            )
        )
        email_confirmation_token = await self.session.execute(q)
        return email_confirmation_token.scalars().one_or_none()
