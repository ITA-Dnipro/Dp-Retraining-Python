from unittest.mock import AsyncMock

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from common.tests.generics import TestMixin
from common.tests.test_data.users import user_pictures_mock_data
from users.models import UserPicture
from users.utils.aws_s3 import S3Client, S3EventHandler
from users.utils.aws_s3.user_pictures import UserImageFile


class TestCaseS3HandlerValidData(TestMixin):

    @pytest.mark.asyncio
    async def test_S3Handler_upload_image_to_s3_valid_test_data(
            self, db_session: AsyncSession, test_S3Client: S3Client, test_user_image_file: UserImageFile,
            mock_upload_file_object: AsyncMock, test_user_picture: UserPicture,
    ) -> None:
        """Test 'S3Handler.upload_image_to_s3()' method with valid incoming test data and mocked valid response.

        Args:
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_S3Client: pytest fixture, creates valid S3Client object.
            test_user_image_file: pytest fixture, creates valid UserImageFile object.
            mock_upload_file_object: pytest fixture, creates mocked 'S3Client.upload_file_object()' method.
            test_user_picture: pytest fixture, add user picture to database.

        Returns:
        Nothing.
        """
        s3_handler = S3EventHandler(
            s3_client=test_S3Client,
            db_session=db_session,
            user_image_file=test_user_image_file,
        )
        await s3_handler.upload_image_to_s3()
        expected_url = user_pictures_mock_data.S3Client_upload_image_to_s3_valid_response['uploaded_file_url']
        expected_etag = user_pictures_mock_data.S3Client_upload_image_to_s3_valid_response['ETag']
        assert test_user_picture.url == expected_url
        assert test_user_picture.etag == expected_etag
        assert (await db_session.execute(select(func.count(UserPicture.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_S3Handler_update_image_in_s3_valid_test_data(
            self, db_session: AsyncSession, test_S3Client: S3Client, test_user_image_file: UserImageFile,
            mock_upload_file_object: AsyncMock, test_user_picture: UserPicture, mock_delete_file_objects: AsyncMock,
    ) -> None:
        """Test 'S3Handler.upload_image_to_s3()' method with valid incoming test data and mocked valid response.

        Args:
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_S3Client: pytest fixture, creates valid S3Client object.
            test_user_image_file: pytest fixture, creates valid UserImageFile object.
            mock_upload_file_object: pytest fixture, creates mocked 'S3Client.upload_file_object()' method.
            test_user_picture: pytest fixture, add user picture to database.
            mock_delete_file_objects: pytest fixture, creates mocked 'S3Client.delete_file_objects()' method.

        Returns:
        Nothing.
        """
        s3_handler = S3EventHandler(
            s3_client=test_S3Client,
            db_session=db_session,
            user_image_file=test_user_image_file,
        )
        await s3_handler.update_image_in_s3()
        expected_url = user_pictures_mock_data.S3Client_upload_image_to_s3_valid_response['uploaded_file_url']
        expected_etag = user_pictures_mock_data.S3Client_upload_image_to_s3_valid_response['ETag']
        assert test_user_picture.url == expected_url
        assert test_user_picture.etag == expected_etag
        assert (await db_session.execute(select(func.count(UserPicture.id)))).scalar_one() == 1
