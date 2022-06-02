from uuid import UUID

from fastapi import status

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from users.cruds.users_crud import UserCRUD
from users.models import UserPicture
from users.schemas.user_pictures import UserPictureUpdateSchema
from users.utils.exceptions import UserPictureNotFoundError
from utils.logging import setup_logging


class UserPictureCRUD(UserCRUD):

    def __init__(self, session: AsyncSession) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def add_user_picture(self, id_: UUID) -> UserPicture:
        """Add UserPicture object to the database.

        Args:
            id_: UUID of User object.

        Returns:
        newly created UserPicture object.
        """
        return await self._add_user_picture(id_)

    async def _add_user_picture(self, id_: UUID) -> UserPicture:
        user = await self._get_user_by_id(id_=id_)
        user_picture = UserPicture(user_id=user.id)
        self.session.add(user_picture)
        await self.session.commit()
        await self.session.refresh(user_picture)
        return user_picture

    async def update_user_picture(self, picture_id: UUID, picture_data: UserPictureUpdateSchema) -> UserPicture:
        """Updates UserPicture object in the database.

        Args:
            picture_id: UUID of UserPicture object.
            picture_data: UserPictureUpdateSchema object.

        Returns:
        Updated UserPicture object from the database.
        """
        return await self._update_user_picture(picture_id, picture_data)

    async def _update_user_picture(self, picture_id: UUID, picture_data: UserPictureUpdateSchema) -> UserPicture:
        await self.session.execute(
            update(UserPicture).where(UserPicture.id == picture_id).values(**picture_data.dict())
        )
        await self.session.commit()
        # Return updated UserPicture.
        self._log.debug(f'''UserPicture with id: "{picture_id}" successfully updated.''')
        return await self._get_user_picture_by_id(id_=picture_id)

    async def get_user_picture_by_id(self, id_: UUID) -> UserPicture:
        """Get UserPicture object from database filtered by id.

        Args:
            id_: UUID of UserPicture object.

        Returns:
        single UserPicture object filtered by id.
        """
        return await self._get_user_picture_by_id(id_)

    async def _get_user_picture_by_id(self, id_: UUID) -> UserPicture:
        self._log.debug(f'''Getting UserPicture with id: "{id_}" from the db.''')
        return await self._select_user_picture(column='id', value=id_)

    async def _select_user_picture(self, column: str, value: UUID | str) -> UserPicture:
        user_picture_exists = await self._user_picture_exists(column=column, value=value)
        if user_picture_exists:
            user_picture = await self.session.execute(
                select(UserPicture).where(UserPicture.__table__.columns[column] == value)
            )
            return user_picture.scalar_one()

    async def _user_picture_exists(self, column: str, value: UUID | str) -> bool:
        user_picture = await self.session.execute(
            select(UserPicture).where(UserPicture.__table__.columns[column] == value)
        )
        try:
            user_picture.one()
        except NoResultFound as err:
            err_msg = f"UserPicture with {column}: '{value}' not found."
            self._log.debug(err_msg)
            self._log.debug(err)
            raise UserPictureNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return True

    async def delete_user_picture(self, id_: UUID) -> None:
        """Delete UserPicture object from the database.

        Args:
            id_: UUID of UserPicture object.

        Returns:
        Nothing.
        """
        return await self._delete_user_picture(id_)

    async def _delete_user_picture(self, id_: UUID) -> None:
        user_picture = await self._get_user_picture_by_id(id_)
        await self.session.delete(user_picture)
        await self.session.commit()
        self._log.debug(f'''UserPicture with id: "{id_}" successfully deleted.''')
