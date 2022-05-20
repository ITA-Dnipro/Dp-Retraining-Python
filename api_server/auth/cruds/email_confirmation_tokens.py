from datetime import datetime
from uuid import UUID
import abc

from sqlalchemy import update

from auth.models import EmailConfirmationToken
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

    @abc.abstractclassmethod
    async def _add_email_confirmation_token(self, id_: UUID, token: str) -> None:
        pass


class EmailConfirmationTokenCRUD(AbstractEmailConfirmationTokenCRUD, UserCRUD):

    async def _add_email_confirmation_token(self, id_: UUID, token: str) -> EmailConfirmationToken:
        user = await self.get_user_by_id(id_=id_)
        await self._expire_existing_email_confirmation_tokens(id_=id_)
        email_confirmation_token = EmailConfirmationToken(user_id=user.id, token=token)
        self.session.add(email_confirmation_token)
        await self.session.commit()
        await self.session.refresh(email_confirmation_token)
        return email_confirmation_token

    async def _expire_existing_email_confirmation_tokens(self, id_: UUID) -> None:
        """Finds all user's non expired tokens and expires them.

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
