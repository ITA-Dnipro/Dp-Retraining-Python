from uuid import UUID
import abc

from fastapi import Depends, UploadFile

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from users.cruds import UserPictureCRUD
from users.models import UserPicture
from users.tasks.user_pictures import save_user_picture_in_aws_s3_bucket
from users.utils.aws_s3.aws_s3 import S3Handler
from users.utils.jwt.user_picture import jwt_user_picture_validator
from users.utils.user_pictures import UserProfileImageValidator
from utils.logging import setup_logging


class AbstractUserPictureService(metaclass=abc.ABCMeta):

    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        Authorize: AuthJWT = Depends(),
    ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.Authorize = Authorize
        self.S3Handler = S3Handler
        self.user_picture_crud = UserPictureCRUD(session=self.session)

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
        # Checking JWT.
        self.Authorize.jwt_required()
        jwt_subject = self.Authorize.get_jwt_subject()
        user = await self.user_picture_crud._get_user_by_id(id_=id_)
        if jwt_user_picture_validator(jwt_subject=jwt_subject, username=user.username):
            # Validating incoming image.
            await UserProfileImageValidator.validate_image(image)
            # Saving UserPicture object.
            user_picture = await self.user_picture_crud._add_user_picture(id_)
            # Starting celery task to save image in AWS S3 bucket.
            save_user_picture_in_aws_s3_bucket.apply_async(
                kwargs={
                    'db_user_picture': user_picture,
                    'image': await image.read(),
                    'content_type': image.content_type,
                    'file_extension': image.filename.split('.')[-1].lower(),
                },
                serializers='pickle',
            )

            return user_picture
