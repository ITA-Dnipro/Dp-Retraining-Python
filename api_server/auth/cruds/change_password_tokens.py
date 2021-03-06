from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, select, update

from auth.models import ChangePasswordToken
from users.cruds.users_crud import UserCRUD
from utils.logging import setup_logging


class ChangePasswordTokenCRUD(UserCRUD):

    def __init__(self, session) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def add_change_password_token(self, id_: UUID, token: str) -> ChangePasswordToken:
        """Add ChangePasswordToken object to the database.

        Args:
            id_: UUID of User object.
            token: string with encoded JWT token.

        Returns:
        newly created ChangePasswordToken object.
        """
        return await self._add_change_password_token(id_, token)

    async def _add_change_password_token(self, id_: UUID, token: str) -> ChangePasswordToken:
        await self._expire_all_existing_change_password_tokens(id_=id_)
        change_password_token = ChangePasswordToken(user_id=id_, token=token)
        self.session.add(change_password_token)
        await self.session.commit()
        await self.session.refresh(change_password_token)
        return change_password_token

    async def _expire_all_existing_change_password_tokens(self, id_: UUID) -> None:
        """Finds all user's non expired tokens and expires them by setting 'expired_at' field with current time.

        Args:
            id_: UUID of a user.

        Returns:
        Nothing.
        """
        q = update(
            ChangePasswordToken
        ).where(
            and_(
                ChangePasswordToken.user_id == id_,
                ChangePasswordToken.expired_at == None, # noqa
            )
        ).values(
            expired_at=datetime.utcnow()
        )
        await self.session.execute(q)
        await self.session.commit()

    async def _select_change_password_token(self, column: str, value: UUID | str) -> ChangePasswordToken:
        change_password_token = await self.session.execute(
            select(ChangePasswordToken).where(ChangePasswordToken.__table__.columns[column] == value),
        )
        return change_password_token.scalars().one_or_none()

    async def _get_change_password_by_token(self, token: str) -> ChangePasswordToken:
        return await self._select_change_password_token(column='token', value=token)

    async def _get_last_non_expired_change_password_token_by_user_id(self, user_id: UUID) -> ChangePasswordToken:
        q = select(
            ChangePasswordToken
        ).where(
            and_(
                ChangePasswordToken.user_id == user_id,
                ChangePasswordToken.expired_at == None, # noqa
            )
        )
        change_password_token = await self.session.execute(q)
        return change_password_token.scalars().one_or_none()

    async def _expire_change_password_token_by_id(self, id_: UUID) -> None:
        """Expires specific ChangePasswordToken object by setting 'expired_at' field with current time.

        Args:
            id_: UUID of ChangePasswordToken object.

        Returns:
        Nothing.
        """
        await self.session.execute(
            update(
                ChangePasswordToken
            ).where(
                ChangePasswordToken.id == id_
            ).values(
                expired_at=datetime.utcnow()
            )
        )
        await self.session.commit()
