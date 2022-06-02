from datetime import datetime
from uuid import UUID

from fastapi import status

from sqlalchemy import func, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from users.models import User
from users.schemas import UserInputSchema, UserUpdateSchema
from users.utils.exceptions import UserNotFoundError
from utils.logging import setup_logging


class UserCRUD:

    def __init__(self, session: AsyncSession) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def get_users(self) -> list[User]:
        """Get User objects from database.

        Returns:
        list of User objects.
        """
        return await self._get_users()

    async def _get_users(self, page: int, page_size: int) -> None:
        self._log.debug('Getting all users from the db.')
        q = select(User).limit(page_size).offset((page - 1) * page_size)
        return (await self.session.execute(q)).scalars().all()

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

    async def get_user_by_id(self, id_: UUID) -> User:
        """Get User object from database filtered by id.

        Args:
            id_: UUID of user.

        Returns:
        single User object filtered by id.
        """
        return await self._get_user_by_id(id_)

    async def _get_user_by_id(self, id_: UUID) -> None:
        self._log.debug(f'''Getting user with id: "{id_}" from the db.''')
        return await self._select_user(column='id', value=id_)

    async def add_user(self, user: UserInputSchema) -> User:
        """Add User object to the database.

        Args:
            user: UserInputSchema object.

        Returns:
        newly created User object.
        """
        return await self._add_user(user)

    async def _add_user(self, user: UserInputSchema) -> User:
        user = User(**user.dict())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        self._log.debug(f'''User with id: "{user.id}" successfully created.''')
        return user

    async def update_user(self, id_: UUID, user: UserUpdateSchema) -> User:
        """Updates User object in the database.

        Args:
            id_: UUID of user.
            user: UserUpdateSchema object.

        Returns:
        updated User object.
        """
        return await self._update_user(id_, user)

    async def _update_user(self, id_: UUID, user: UserUpdateSchema) -> None:
        await self.session.execute(update(User).where(User.id == id_).values(**user.dict()))
        await self.session.commit()
        # Return updated user.
        self._log.debug(f'''User with id: "{id_}" successfully updated.''')
        return await self._get_user_by_id(id_=id_)

    async def delete_user(self, id_: UUID) -> None:
        """Delete User object from the database.

        Args:
            id_: UUID of user.

        Returns:
        Nothing.
        """
        return await self._delete_user(id_)

    async def _delete_user(self, id_: UUID) -> None:
        user = await self._get_user_by_id(id_=id_)
        await self.session.delete(user)
        await self.session.commit()
        self._log.debug(f'''User with id: "{id_}" successfully deleted.''')

    async def get_user_by_username(self, username: str) -> User:
        """Get User object from database filtered by username.

        Args:
            username: string of User's username.

        Returns:
        Single User object filtered by username.
        """
        return await self._get_user_by_username(username)

    async def _get_user_by_username(self, username: str) -> None:
        user = await self._select_user(column='username', value=username)
        return user

    async def get_user_by_email(self, email: str) -> User:
        """Get User object from database filtered by email.

        Args:
            email: string of User's email.

        Returns:
        Single User object filtered by email.
        """
        return await self._get_user_by_email(email)

    async def _get_user_by_email(self, email: str) -> None:
        return await self._select_user(column='email', value=email)

    async def _activate_user_by_id(self, id_: UUID) -> None:
        """Activates User by setting 'activated_at' field with current time.

        Args:
            id_: UUID of User object.

        Returns:
        Nothing.
        """
        await self.session.execute(
            update(
                User
            ).where(
                User.id == id_
            ).values(
                activated_at=datetime.utcnow()
            )
        )
        await self.session.commit()

    async def _get_total_of_users(self) -> int:
        """Counts number of users in User table.

        Returns:
        Quantity of user objects in User table.
        """
        return (await self.session.execute(select(func.count(User.id)))).scalar_one()

    async def _update_user_password(self, id_, pass_hash: str) -> None:
        """Updates user's 'password' field data in table.

        Args:
            id_: UUID of user.
            pass_hash: hashed password string.

        Returns:
        Nothing.
        """
        await self.session.execute(
            update(
                User
            ).where(
                User.id == id_
            ).values(
                password=pass_hash
            )
        )
        await self.session.commit()
