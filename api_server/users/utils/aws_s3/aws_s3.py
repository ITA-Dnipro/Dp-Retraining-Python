from uuid import UUID

from fastapi import status

from aiobotocore.session import get_session
from botocore.exceptions import ClientError

from common.constants.users import S3ClientConstants
from utils.logging import setup_logging


class S3Client:
    """Helper class to handle requests and responses to AWS S3."""

    def __init__(
            self,
            aws_access_key_id: str = None,
            aws_secret_access_key: str = None,
            aws_s3_bucket_name: str = None,
            aws_s3_bucket_region: str = None,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_s3_bucket_name = aws_s3_bucket_name
        self.aws_s3_bucket_region = aws_s3_bucket_region
        self._log = setup_logging(self.__class__.__name__)

    async def upload_file_object(
            self, file_name: str = None, content_type: str = None, file_obj: bytes = None,
    ) -> dict:
        """Uploads fastapi UploadFile to AWS S3 bucket.

        Args:
            file_name: string with full file path on AWS S3 bucket.
            content_type: file's content type.
            file_obj: file object to upload in AWS S3 bucket.

        Returns:
        A dict with AWS S3 response.
        """
        session = get_session()
        async with session.create_client(
                S3ClientConstants.S3_NAME.value,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_access_key_id=self.aws_access_key_id,
        ) as client:
            try:
                response = await client.put_object(
                    Bucket=self.aws_s3_bucket_name,
                    Key=file_name,
                    Body=file_obj,
                    ACL=S3ClientConstants.ACL_PUBLIC_READ.value,
                    ContentType=content_type,
                )
            except ClientError as exc:
                self._log.warning(exc)
                raise exc
            if response['ResponseMetadata']['HTTPStatusCode'] == status.HTTP_200_OK:
                self._log.debug(S3ClientConstants.SUCCESSFUL_UPLOAD_MSG.value.format(
                    bucket_name=self.aws_s3_bucket_name,
                    bucket_region=self.aws_s3_bucket_region,
                    file_name=file_name,
                    )
                )
                response['uploaded_file_url'] = S3ClientConstants.UPLOADED_FILE_URL.value.format(
                    bucket_name=self.aws_s3_bucket_name,
                    bucket_region=self.aws_s3_bucket_region,
                    file_name=file_name,
                )

            return response

    async def delete_file_objects(self, user_id: UUID) -> dict:
        """Deletes all file objects in user profile_pics folder.

        Args:
            user_id: UUID of user.

        Returns:
        A dict with AWS S3 response.
        """
        session = get_session()
        async with session.create_client(
                S3ClientConstants.S3_NAME.value,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_access_key_id=self.aws_access_key_id,
        ) as client:
            user_folder = S3ClientConstants.USER_PROFILE_PICS_FOLDER_NAME.value.format(
                user_id=user_id,
            )
            paginator = client.get_paginator('list_objects')
            async for result in paginator.paginate(Bucket=self.aws_s3_bucket_name, Prefix=user_folder):
                for user_picture in result.get('Contents', []):
                    try:
                        response = await client.delete_object(
                            Bucket=self.aws_s3_bucket_name,
                            Key=user_picture['Key']
                        )
                    except ClientError as exc:
                        self._log.warning(exc)
                        raise exc
                    if response['ResponseMetadata']['HTTPStatusCode'] == status.HTTP_204_NO_CONTENT:
                        self._log.debug(S3ClientConstants.SUCCESSFUL_DELETE_MSG.value.format(
                            file_path=user_picture['Key']),
                        )
            return response
