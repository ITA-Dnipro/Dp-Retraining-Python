from datetime import datetime
from uuid import UUID

from sqlalchemy import func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from users.models import User
from users.schemas import UserInputSchema, UserUpdateSchema
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

    async def _select_user(self, column: str, value: UUID | str) -> None:
        self._log.debug(f'Getting user with "{column}": "{value}" from the db.')
        user = await self.session.execute(select(User).where(User.__table__.columns[column] == value))
        return user.scalars().one_or_none()

    async def get_user_by_id(self, id_: UUID) -> User:
        """Get User object from database filtered by id.

        Args:
            id_: UUID of user.

        Returns:
        single User object filtered by id.
        """
        return await self._get_user_by_id(id_)

    async def _get_user_by_id(self, id_: UUID) -> None:
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
        self._log.debug(f'User with id: "{id_}" successfully updated.')
        return await self._get_user_by_id(id_=id_)

    async def delete_user(self, id_: UUID) -> None:
        """Delete User object from the database.

        Args:
            id_: UUID of user.

        Returns:
        Nothing.
        """
        return await self._delete_user(id_)

    async def _delete_user(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
        self._log.debug(f'User with id: "{user.id}" successfully deleted.')

    async def get_user_by_username(self, username: str) -> User:
        """Get User object from database filtered by username.

        Args:
            username: string of User's username.

        Returns:
        Single User object filtered by username.
        """
        return await self._get_user_by_username(username)

    async def _get_user_by_username(self, username: str) -> None:
        return await self._select_user(column='username', value=username)

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
        self._log.debug(f'User with id: "{id_}" successfully activated.')

    async def _get_total_of_users(self) -> int:
        """Counts number of users in User table.

        Returns:
        Quantity of user objects in User table.
        """
        total_users = (await self.session.execute(select(func.count(User.id)))).scalar_one()
        self._log.debug(f'User table has totally: "{total_users}" users.')
        return total_users

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
        self._log.debug(f'User with id: "{id_}" successfully updated password.')
