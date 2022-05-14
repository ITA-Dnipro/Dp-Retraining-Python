from fastapi import Request, UploadFile

from aiobotocore.session import get_session

from common.constants.users import S3HandlerConstants
from utils.logging import setup_logging


class S3Handler:

    def __init__(
            self,
            request: Request,
            aws_access_key_id: str = None,
            aws_secret_access_key: str = None,
            aws_s3_bucket_name: str = None,
            aws_s3_bucket_region: str = None,
    ):
        self.aws_access_key_id = request.app.app_config.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = request.app.app_config.AWS_SECRET_ACCESS_KEY
        self.aws_s3_bucket_name = request.app.app_config.AWS_S3_BUCKET_NAME
        self.aws_s3_bucket_region = request.app.app_config.AWS_S3_BUCKET_REGION
        self._log = setup_logging(self.__class__.__name__)

    async def upload_file_object(
            self, file_name: str = None, content_type: str = None, file_obj: UploadFile = None,
    ) -> None:
        """Uploads fastapi UploadFile to AWS S3 bucket.

        Args:
            file_name: string with full file path on AWS S3 bucket.
            file_obj: UploadFile to upload in AWS S3 bucket.

        Returns:
        Nothing.
        """
        # Important step to get file ready to upload.
        await file_obj.seek(0)
        session = get_session()
        async with session.create_client(
                S3HandlerConstants.S3_NAME.value,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_access_key_id=self.aws_access_key_id
        ) as client:
            await client.put_object(
                Bucket=self.aws_s3_bucket_name,
                Key=file_name,
                Body=await file_obj.read(),
                ACL=S3HandlerConstants.ACL_PUBLIC_READ.value,
                ContentType=content_type,
            )
            self._log.debug(S3HandlerConstants.SUCCESSFUL_UPLOAD_MSG.value.format(
                bucket_name=self.aws_s3_bucket_name,
                bucket_region=self.aws_s3_bucket_region,
                file_name=file_name,
                )
            )
