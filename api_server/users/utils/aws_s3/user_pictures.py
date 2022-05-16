from datetime import datetime
from typing import AsyncContextManager
from uuid import UUID

from common.constants.users import S3ClientConstants
from users.cruds import UserPictureCRUD
from users.models import UserPicture
from users.schemas.user_pictures import UserPictureUpdateSchema
from users.utils.aws_s3.aws_s3 import S3Client


class UserImageFile:
    """Container object for UserPicture object attributes."""

    def __init__(self, db_user_picture: UserPicture, image_data: bytes,  content_type: str, file_extension: str):
        self.db_user_picture = db_user_picture
        self.image_data = image_data
        self.content_type = content_type
        self.file_extension = file_extension

    @property
    def file_name(self):
        return S3ClientConstants.PICTURE_FILE_NAME.value.format(
            user_id=self.db_user_picture.user_id,
            picture_id=self.db_user_picture.id,
            file_extension=self.file_extension,
        )


class S3EventHandler:
    """Helper class to handle S3 events such as upload, delete files in AWS S3."""

    def __init__(
            self,
            s3_client: S3Client,
            db_session: AsyncContextManager,
            user_image_file: UserImageFile | None = None,
    ):
        self.s3_client = s3_client
        self.user_image_file = user_image_file
        self.db_session = db_session

    async def upload_image_to_s3(self) -> UserPicture:
        """Uploads user's image to AWS S3 bucket and saves additional info in UserPicture model.

        Returns:
        Updated UserPicture object with image's S3 information.
        """
        response = await self._upload_image_to_s3()
        return await self._save_uploaded_image_data(s3_response=response)

    async def _upload_image_to_s3(self) -> dict:
        """Uploads file to AWS S3 bucket.

        Returns:
        dict with AWS S3 response.
        """
        return await self.s3_client.upload_file_object(
            content_type=self.user_image_file.content_type,
            file_obj=self.user_image_file.image_data,
            file_name=self.user_image_file.file_name,
        )

    async def _save_uploaded_image_data(self, s3_response: dict) -> UserPicture:
        """Saves additional UserPicture data in the database.

        Args:
            s3_response: dict with response data from AWS S3.

        Returns:
        Updated UserPicture object.
        """
        formatted_updated_at_datetime = datetime.strptime(
            s3_response['ResponseMetadata']['HTTPHeaders']['date'],
            S3ClientConstants.AWS_S3_RESPONSE_DATETIME_FORMAT.value,
        )
        user_picture_update_data = UserPictureUpdateSchema(
            url=s3_response['uploaded_file_url'],
            updated_at=formatted_updated_at_datetime,
            etag=s3_response['ETag'],
        )
        async with self.db_session as session:
            user_picture_crud = UserPictureCRUD(session=session)
            return await user_picture_crud.update_user_picture(
                picture_id=self.user_image_file.db_user_picture.id,
                picture_data=user_picture_update_data,
            )

    async def update_image_in_s3(self) -> UserPicture:
        """Deletes Previously uploaded user's image and uploads new user's image.

        Returns:
        Updated UserPicture object with image's S3 information.
        """
        await self._delete_images_in_s3(user_id=self.user_image_file.db_user_picture.user_id)
        return await self.upload_image_to_s3()

    async def delete_images_in_s3(self, user_id: UUID) -> dict:
        """Delete all files in user's folder in AWS S3 bucket.

        Args:
            user_id: UUID of User object.

        Returns:
        dict with AWS S3 response.
        """
        return await self._delete_images_in_s3(user_id)

    async def _delete_images_in_s3(self, user_id: UUID) -> dict:
        return await self.s3_client.delete_file_objects(user_id)
