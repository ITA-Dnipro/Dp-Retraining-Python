from uuid import UUID
import asyncio

from app.celery_base import app
from db import create_engine
from users.models import UserPicture
from users.utils.aws_s3 import S3Client
from users.utils.aws_s3.user_pictures import S3EventHandler, UserImageFile
from utils.orm_helpers import create_db_session


@app.task
def save_user_picture_in_aws_s3_bucket(
    db_user_picture: UserPicture, image_data: bytes, content_type: str, file_extension: str,
        ) -> UserPicture:
    """Background celery task saving user's uploaded image to AWS S3 bucket.

    Args:
        db_user_picture: UserPicture instance.
        image_data: bytes content of uploaded image.
        content_type: image's content-type.
        file_extension: image file extension.

    Returns:
    Updated UserPicture object.
    """
    s3_client = S3Client(
        aws_access_key_id=app.conf.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=app.conf.get('AWS_SECRET_ACCESS_KEY'),
        aws_s3_bucket_region=app.conf.get('AWS_S3_BUCKET_REGION'),
        aws_s3_bucket_name=app.conf.get('AWS_S3_BUCKET_NAME'),
    )
    user_image_file = UserImageFile(
        db_user_picture=db_user_picture,
        image_data=image_data,
        content_type=content_type,
        file_extension=file_extension,
    )
    engine = create_engine(
        database_url=app.conf.get('POSTGRES_DATABASE_URL'),
        echo=app.conf.get('API_SQLALCHEMY_ECHO'),
        future=app.conf.get('API_SQLALCHEMY_FUTURE'),
    )
    db_session = create_db_session(engine=engine)
    s3_event_handler = S3EventHandler(s3_client=s3_client, user_image_file=user_image_file, db_session=db_session)
    return asyncio.run(s3_event_handler.upload_image_to_s3())


@app.task()
def update_user_picture_in_aws_s3_bucket(
    db_user_picture: UserPicture, image_data: bytes, content_type: str, file_extension: str,
        ) -> UserPicture:
    """Background celery task updating user's uploaded image in the AWS S3 bucket.

    Args:
        db_user_picture: UserPicture instance.
        image_data: bytes content of uploaded image.
        content_type: image's content-type.
        file_extension: image file extension.

    Returns:
    Updated UserPicture object.
    """
    s3_client = S3Client(
        aws_access_key_id=app.conf.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=app.conf.get('AWS_SECRET_ACCESS_KEY'),
        aws_s3_bucket_region=app.conf.get('AWS_S3_BUCKET_REGION'),
        aws_s3_bucket_name=app.conf.get('AWS_S3_BUCKET_NAME'),
    )
    user_image_file = UserImageFile(
        db_user_picture=db_user_picture,
        image_data=image_data,
        content_type=content_type,
        file_extension=file_extension,
    )
    engine = create_engine(
        database_url=app.conf.get('POSTGRES_DATABASE_URL'),
        echo=app.conf.get('API_SQLALCHEMY_ECHO'),
        future=app.conf.get('API_SQLALCHEMY_FUTURE'),
    )
    db_session = create_db_session(engine=engine)
    s3_event_handler = S3EventHandler(s3_client=s3_client, user_image_file=user_image_file, db_session=db_session)
    return asyncio.run(s3_event_handler.update_image_in_s3())


@app.task
def delete_user_picture_in_aws_s3_bucket(user_id: UUID) -> bool:
    """Background celery task deletes user's uploaded image in the AWS S3 bucket.

    Args:
        user_id: UUID of User object.

    Returns:
    bool as task result.
    """
    s3_client = S3Client(
        aws_access_key_id=app.conf.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=app.conf.get('AWS_SECRET_ACCESS_KEY'),
        aws_s3_bucket_region=app.conf.get('AWS_S3_BUCKET_REGION'),
        aws_s3_bucket_name=app.conf.get('AWS_S3_BUCKET_NAME'),
    )
    engine = create_engine(
        database_url=app.conf.get('POSTGRES_DATABASE_URL'),
        echo=app.conf.get('API_SQLALCHEMY_ECHO'),
        future=app.conf.get('API_SQLALCHEMY_FUTURE'),
    )
    db_session = create_db_session(engine=engine)
    s3_event_handler = S3EventHandler(s3_client, db_session)
    return asyncio.run(s3_event_handler.delete_images_in_s3(user_id))
