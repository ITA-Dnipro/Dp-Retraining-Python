from datetime import datetime
from uuid import UUID
import abc

from fastapi import status

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from auth.models import ChangePasswordToken
from auth.utils.exceptions import ChangePasswordTokenNotFoundError
from users.cruds.users_crud import UserCRUD
from utils.logging import setup_logging


class AbstractChangePasswordTokenCRUD(metaclass=abc.ABCMeta):

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

    @classmethod
    async def _add_change_password_token(self, id_: UUID, token: str) -> None:
        pass


class ChangePasswordTokenCRUD(AbstractChangePasswordTokenCRUD, UserCRUD):

    async def _add_change_password_token(self, id_: UUID, token: str) -> ChangePasswordToken:
        user = await self.get_user_by_id(id_=id_)
        await self._expire_all_existing_change_password_tokens(id_=id_)
        change_password_token = ChangePasswordToken(user_id=user.id, token=token)
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
        await self.session.execute(
            update(
                ChangePasswordToken
            ).where(
                ChangePasswordToken.user_id == id_
            ).where(
                ChangePasswordToken.expired_at == None # noqa
            ).values(
                expired_at=datetime.utcnow()
            )
        )
        await self.session.commit()

    async def _change_password_token_exists(self, column: str, value: UUID | str) -> bool:
        change_password_token = await self.session.execute(
            select(ChangePasswordToken).where(ChangePasswordToken.__table__.columns[column] == value),
        )
        try:
            change_password_token.one()
        except NoResultFound as err:
            err_msg = f"ChangePasswordToken with {column}: '{value}' not found."
            self._log.debug(err_msg)
            self._log.debug(err)
            raise ChangePasswordTokenNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return True

    async def _select_change_password_token(self, column: str, value: UUID | str) -> ChangePasswordToken:
        change_password_token_exists = await self._change_password_token_exists(column=column, value=value)
        if change_password_token_exists:
            change_password_token = await self.session.execute(
                select(ChangePasswordToken).where(ChangePasswordToken.__table__.columns[column] == value),
            )
            return change_password_token.scalar_one()

    async def _get_change_password_by_token(self, token: str) -> ChangePasswordToken:
        return await self._select_email_confirmation_token(column='token', value=token)

    async def _get_last_non_expired_change_password_token_by_user_id(self, user_id: UUID) -> ChangePasswordToken:
        q = select(
            ChangePasswordToken
        ).where(
            ChangePasswordToken.user_id == user_id
        ).where(
            ChangePasswordToken.expired_at == None # noqa
        )
        change_password_token = await self.session.execute(q)
        return change_password_token.scalars().one_or_none()
