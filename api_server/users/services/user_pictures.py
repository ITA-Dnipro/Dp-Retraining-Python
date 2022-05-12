from uuid import UUID
import abc

from fastapi import Depends, UploadFile

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from users.models import UserPicture
from users.services import UserService
from users.services.aws_s3 import S3Handler
from users.utils.jwt import jwt_user_validator
from utils.logging import setup_logging


class AbstractUserPictureService(metaclass=abc.ABCMeta):

    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        Authorize: AuthJWT = Depends(),
        S3Handler: S3Handler = Depends(),
        user_service: UserService = Depends(),
    ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.Authorize = Authorize
        self.S3Handler = S3Handler
        self.user_service = user_service

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


class UserPictureService(AbstractUserPictureService):

    async def _add_user_picture(self, id_: UUID, image: UploadFile | None) -> UserPicture:
        # Checking JWT credentials.
        self.Authorize.jwt_required()
        jwt_subject = self.Authorize.get_jwt_subject()
        user = await self.user_service._get_user_by_id(id_=id_)
        if jwt_user_validator(jwt_subject=jwt_subject, username=user.username):
            # Checking uploaded image.
            await self.user_service._validate_image(image)
            # Creating UserPicture object.
            user_picture = UserPicture(user_id=user.id)
            self.session.add(user_picture)
            await self.session.commit()
            await self.session.refresh(user_picture)
            # TODO: AWS S3 image saving here.
            return user_picture
