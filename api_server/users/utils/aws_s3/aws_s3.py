from aiobotocore.session import get_session
from botocore.exceptions import ClientError

from common.constants.users import S3HandlerConstants
from utils.logging import setup_logging


class S3Handler:
    """Helper class to make requests in AWS S3."""

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
    ) -> None:
        """Uploads fastapi UploadFile to AWS S3 bucket.

        Args:
            file_name: string with full file path on AWS S3 bucket.
            file_obj: file to upload in AWS S3 bucket.

        Returns:
        Nothing.
        """
        session = get_session()
        async with session.create_client(
                S3HandlerConstants.S3_NAME.value,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_access_key_id=self.aws_access_key_id
        ) as client:
            try:
                response = await client.put_object(
                    Bucket=self.aws_s3_bucket_name,
                    Key=file_name,
                    Body=file_obj,
                    ACL=S3HandlerConstants.ACL_PUBLIC_READ.value,
                    ContentType=content_type,
                )
            except ClientError as exc:
                self._log.warning(exc)
                raise exc
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                self._log.debug(S3HandlerConstants.SUCCESSFUL_UPLOAD_MSG.value.format(
                    bucket_name=self.aws_s3_bucket_name,
                    bucket_region=self.aws_s3_bucket_region,
                    file_name=file_name,
                    )
                )
                response['uploaded_file_url'] = S3HandlerConstants.UPLOADED_FILE_URL.value.format(
                    bucket_name=self.aws_s3_bucket_name,
                    bucket_region=self.aws_s3_bucket_region,
                    file_name=file_name,
                )

            return response
