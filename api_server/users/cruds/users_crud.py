from uuid import UUID
import abc

from fastapi import status

from passlib.hash import argon2
from sqlalchemy import update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select

from users.models import User
from users.schemas import UserInputSchema, UserUpdateSchema
from users.utils.exceptions import UserNotFoundError
from utils.logging import setup_logging


class AbstractUserCRUD(metaclass=abc.ABCMeta):

    def __init__(self, session) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

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


class UserCRUD(AbstractUserCRUD):

    async def _get_users(self) -> None:
        self._log.debug('Getting all users from the db.')
        users = await self.session.execute(select(User))
        return users.scalars().all()

    async def _user_exists(self, column: str, value: UUID | str) -> bool:
        user = await self.session.execute(select(User).where(User.__table__.columns[column] == value))
        try:
            user.one()
        except NoResultFound as err:
            err_msg = f"User with {column}: '{value}' not found."
            self._log.debug(err_msg)
            self._log.debug(err)
            raise UserNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return True

    async def _select_user(self, column: str, value: UUID | str) -> None:
        user_exists = await self._user_exists(column=column, value=value)
        if user_exists:
            user = await self.session.execute(select(User).where(User.__table__.columns[column] == value))
            return user.scalar_one()

    async def _get_user_by_id(self, id_: UUID) -> None:
        self._log.debug(f'''Getting user with id: "{id_}" from the db.''')
        return await self._select_user(column='id', value=id_)

    async def _add_user(self, user: UserInputSchema) -> User:
        user.password = await self._hash_password(user.password)
        user = User(**user.dict())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        self._log.debug(f'''User with id: "{user.id}" successfully created.''')
        return user

    async def _update_user(self, id_: UUID, user: UserUpdateSchema) -> None:
        await self.session.execute(update(User).where(User.id == id_).values(**user.dict()))
        await self.session.commit()
        # Return updated user.
        self._log.debug(f'''User with id: "{id_}" successfully updated.''')
        return await self._get_user_by_id(id_=id_)

    async def _delete_user(self, id_: UUID) -> None:
        user = await self._get_user_by_id(id_=id_)
        await self.session.delete(user)
        await self.session.commit()
        self._log.debug(f'''User with id: "{id_}" successfully deleted.''')

    async def _hash_password(self, password: str) -> str:
        """Return password hashed with argon2 algorithm."""
        password_hash = argon2.using(rounds=4).hash(password)
        return password_hash

    async def _get_user_by_username(self, username: str) -> None:
        user = await self._select_user(column='username', value=username)
        return user
