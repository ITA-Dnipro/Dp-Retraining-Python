from uuid import UUID
import abc

from fastapi import UploadFile

from users.cruds.users_crud import UserCRUD
from users.models import UserPicture
from utils.logging import setup_logging


class AbstractUserPictureCRUD(metaclass=abc.ABCMeta):

    def __init__(self, session) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def add_user_picture(self, id_: UUID, image: UploadFile | None) -> UserPicture:
        """Add UserPicture object to the database.

        Args:
            id_: UUID of User object.
            image: Uploaded user's image.

        Returns:
        newly created UserPicture object.
        """
        return await self._add_user_picture(id_, image)

    @abc.abstractclassmethod
    async def _add_user_picture(self, id_: UUID, image: UploadFile | None) -> None:
        pass


class UserPictureCRUD(AbstractUserPictureCRUD, UserCRUD):

    async def _add_user_picture(self, id_: UUID) -> UserPicture:
        user = await self._get_user_by_id(id_=id_)
        user_picture = UserPicture(user_id=user.id)
        self.session.add(user_picture)
        await self.session.commit()
        await self.session.refresh(user_picture)
        return user_picture
