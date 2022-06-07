from uuid import UUID

from fastapi import Depends, UploadFile, status

from sqlalchemy.ext.asyncio import AsyncSession

from common.exceptions.users import UserPictureExceptionMsgs
from db import get_session
from users.cruds import UserPictureCRUD
from users.models import UserPicture
from users.services.users import UserService
from users.tasks.user_pictures import (
    delete_user_picture_in_aws_s3_bucket,
    save_user_picture_in_aws_s3_bucket,
    update_user_picture_in_aws_s3_bucket,
)
from users.utils.exceptions import UserPictureNotFoundError
from users.utils.jwt.user_picture import jwt_user_picture_validator
from users.utils.user_pictures import UserProfileImageValidator
from utils.logging import setup_logging


class UserPictureService(UserService):

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session)
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.user_picture_crud = UserPictureCRUD(session=self.session)

    async def add_user_picture(self, id_: UUID, image: UploadFile, jwt_subject: str) -> UserPicture:
        """Add UserPicture object to the database.

        Args:
            id_: UUID of User object.
            image: Uploaded user's image.
            jwt_subject: User's username from jwt token identity.

        Returns:
        newly created UserPicture object.
        """
        return await self._add_user_picture(id_, image, jwt_subject)

    async def _add_user_picture(self, id_: UUID, image: UploadFile, jwt_subject: str) -> UserPicture:
        user = await self.get_user_by_id(id_=id_)
        if jwt_user_picture_validator(jwt_subject=jwt_subject, username=user.username):
            # Validating incoming image.
            await UserProfileImageValidator.validate_image(image)
            # Saving UserPicture object.
            user_picture = await self.user_picture_crud.add_user_picture(id_)
            # Starting celery task to save image in AWS S3 bucket.
            await image.seek(0)
            save_user_picture_in_aws_s3_bucket.apply_async(
                kwargs={
                    'db_user_picture': user_picture,
                    'image_data': await image.read(),
                    'content_type': image.content_type,
                    'file_extension': image.filename.split('.')[-1].lower(),
                },
                serializers='pickle',
            )

            return user_picture

    async def update_user_picture(
            self, id_: UUID, picture_id: UUID, image: UploadFile, jwt_subject: str,
    ) -> UserPicture:
        """Updates user's image in AWS S3 bucket and UserPicture in the database.

        Args:
            id_: UUID of a User object.
            picture_id: UUID of a UserPicture object.
            image: Uploaded user's image.
            jwt_subject: User's username from jwt token identity.

        Returns:
        updated UserPicture object.
        """
        return await self._update_user_picture(id_, picture_id, image, jwt_subject)

    async def _update_user_picture(
            self, id_: UUID, picture_id: UUID, image: UploadFile, jwt_subject: str,
    ) -> UserPicture:
        user = await self.get_user_by_id(id_=id_)
        if jwt_user_picture_validator(jwt_subject=jwt_subject, username=user.username):
            # Validating incoming image.
            await UserProfileImageValidator.validate_image(image)
            user_picture = await self.get_user_picture_by_id(picture_id)
            # Starting celery task to update image in AWS S3 bucket.
            await image.seek(0)
            update_user_picture_in_aws_s3_bucket.apply_async(
                kwargs={
                    'db_user_picture': user_picture,
                    'image_data': await image.read(),
                    'content_type': image.content_type,
                    'file_extension': image.filename.split('.')[-1].lower(),
                },
                serializers='pickle',
            )
            return user_picture

    async def get_user_picture_by_id(self, picture_id: UUID) -> UserPicture:
        """Get UserPicture object from database filtered by id.

        Args:
            picture_id: UUID of UserPicture object.

        Returns:
        A single UserPicture object filtered by id.
        """
        return await self._get_user_picture_by_id(picture_id)

    async def _get_user_picture_by_id(self, picture_id: UUID) -> UserPicture:
        user_picture = await self.user_picture_crud.get_user_picture_by_id(picture_id)
        if not user_picture:
            err_msg = UserPictureExceptionMsgs.USER_PICTURE_NOT_FOUND.value.format(
                column='id',
                value=picture_id,
            )
            self._log.debug(err_msg)
            raise UserPictureNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return user_picture

    async def delete_user_picture(self, id_: UUID, picture_id: UUID, jwt_subject: str) -> None:
        """Delete UserPicture object from the database.

        Args:
            id_: UUID of a User object.
            picture_id: UUID of UserPicture object.
            jwt_subject: User's username from jwt token identity.

        Returns:
        Nothing.
        """
        return await self._delete_user_picture(id_, picture_id, jwt_subject)

    async def _delete_user_picture(self, id_: UUID, picture_id: UUID, jwt_subject: str) -> None:
        user = await self.get_user_by_id(id_)
        if jwt_user_picture_validator(jwt_subject=jwt_subject, username=user.username):
            user_picture = await self.get_user_picture_by_id(picture_id)
            await self.user_picture_crud.delete_user_picture(user_picture)
            # Starting celery task to delete image in AWS S3 bucket.
            delete_user_picture_in_aws_s3_bucket.apply_async(
                kwargs={'user_id': user.id},
                serializers='pickle',
            )
