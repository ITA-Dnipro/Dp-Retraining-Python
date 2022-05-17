from uuid import UUID
import abc

from fastapi import Depends

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from users.cruds import UserCRUD
from users.models import User
from users.schemas import UserInputSchema, UserUpdateSchema
from users.utils.jwt.user import jwt_user_validator
from utils.logging import setup_logging


class AbstractUserService(metaclass=abc.ABCMeta):

    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        Authorize: AuthJWT = Depends(),
    ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.Authorize = Authorize
        self.user_crud = UserCRUD(session=self.session)

    async def get_users(self) -> list[User]:
        """Get User objects from database.

        Returns:
        list of User objects.
        """
        return await self._get_users()

    async def get_user_by_id(self, id_: UUID) -> User:
        """Get User object from database filtered by id.

        Args:
            id_: UUID of user.

        Returns:
        single User object filtered by id.
        """
        return await self._get_user_by_id(id_)

    async def add_user(self, user: UserInputSchema) -> User:
        """Add User object to the database.

        Args:
            user: UserInputSchema object.

        Returns:
        newly created User object.
        """
        return await self._add_user(user)

    async def update_user(self, id_: UUID, user: UserUpdateSchema) -> User:
        """Updates User object in the database.

        Args:
            id_: UUID of user.
            user: UserUpdateSchema object.

        Returns:
        updated User object.
        """
        return await self._update_user(id_, user)

    async def delete_user(self, id_: UUID) -> None:
        """Delete User object from the database.

        Args:
            id_: UUID of user.

        Returns:
        Nothing.
        """
        return await self._delete_user(id_)

    async def get_user_by_username(self, username: str) -> User:
        """Get User object from database filtered by username.

        Args:
            username: string of User's username.

        Returns:
        Single User object filtered by username.
        """
        return await self._get_user_by_username(username)

    @abc.abstractclassmethod
    async def _get_users(self) -> None:
        pass

    @abc.abstractclassmethod
    async def _get_user_by_id(self, id_: UUID) -> None:
        pass

    @abc.abstractclassmethod
    async def _add_user(self, user: UserInputSchema) -> None:
        pass

    @abc.abstractclassmethod
    async def _update_user(self, id_: UUID, user: UserUpdateSchema) -> None:
        pass

    @abc.abstractclassmethod
    async def _delete_user(self, id_: UUID) -> None:
        pass

    @abc.abstractclassmethod
    async def _get_user_by_username(self, username: str) -> None:
        pass


class UserService(AbstractUserService):

    async def _get_users(self) -> None:
        return await self.user_crud._get_users()

    async def _get_user_by_id(self, id_: str) -> None:
        return await self.user_crud._get_user_by_id(id_)

    async def _add_user(self, user: UserInputSchema) -> User:
        return await self.user_crud._add_user(user)

    async def _update_user(self, id_: str, user: UserUpdateSchema) -> None:
        self.Authorize.jwt_required()
        jwt_subject = self.Authorize.get_jwt_subject()
        user_exists = await self.user_crud._select_user(column='id', value=id_)
        if user_exists:
            if jwt_user_validator(jwt_subject=jwt_subject, username=user_exists.username):
                # Updating user.
                return await self.user_crud.update_user(id_, user)

    async def _delete_user(self, id_) -> None:
        self.Authorize.jwt_required()
        jwt_subject = self.Authorize.get_jwt_subject()
        user_exists = await self.user_crud._select_user(column='id', value=id_)
        if user_exists:
            if jwt_user_validator(jwt_subject=jwt_subject, username=user_exists.username):
                # Deleting user.
                return await self.user_crud.delete_user(id_)

    async def _get_user_by_username(self, username: str) -> None:
        return await self.user_crud._select_user(column='username', value=username)