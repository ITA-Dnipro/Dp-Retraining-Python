from datetime import datetime
import asyncio

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api_server.celery_app import app
from common.constants.users import S3HandlerConstants
from db import create_engine
from users.models import UserPicture
from users.utils.aws_s3 import S3Handler


async def create_db_session(engine: AsyncEngine) -> AsyncSession:
    """Creates sqlalchemy AsyncSession instance.

    Args:
        engine: instance of sqlalchemy AsyncEngine.

    Returns:
    An instance of AsyncSession.
    """
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False,
    )
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            await engine.dispose()


async def upload_image_to_s3(s3_handler: S3Handler, content_type: str, file_obj: bytes, file_name: str) -> dict:
    """Uploads file to AWS S3 bucket.

    Args:
        s3_handler: instance of handeler class to make the file upload.
        content_type: uploaded file content type.
        file_obj: file to upload in AWS S3 bucket.
        file_name: file's filename.

    Returns:
    dict with AWS S3 response.
    """
    return await s3_handler.upload_file_object(content_type=content_type, file_obj=file_obj, file_name=file_name)


async def save_uploaded_image_data(
    db_session: AsyncSession, db_user_picture: UserPicture, upload_file_response: dict,
        ) -> bool:
    """Saves additional UserPicture data in the database.

    Args:
        db_session: sqlalchemy db session.
        db_user_picture: instance of UserPicture.
        upload_file_response: dict with response data from AWS S3.

    Returns:
    bool.
    """
    clean_date = datetime.strptime(
        upload_file_response['ResponseMetadata']['HTTPHeaders']['date'],
        S3HandlerConstants.AWS_S3_RESPONSE_DATETIME_FORMAT.value,
    )
    session = await anext(db_session)
    await session.execute(
        update(UserPicture).where(UserPicture.id == db_user_picture.id).values(
            url=upload_file_response['uploaded_file_url'],
            updated_at=clean_date,
        )
    )
    await session.commit()
    return True


@app.task
def save_user_picture_in_aws_s3_bucket(
    db_user_picture: UserPicture, image: bytes, content_type: str, file_extension: str,
        ) -> bool:
    """Background celery task saving user's uploaded image to AWS S3 bucket.

    Args:
        db_user_picture: UserPicture instance.
        image: bytes content of uploaed image.
        content_type: image's content-type.
        file_extension: image file extension.

    Returns:
    Nothing.
    """
    s3_handler = S3Handler(
        aws_access_key_id=app.conf.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=app.conf.get('AWS_SECRET_ACCESS_KEY'),
        aws_s3_bucket_region=app.conf.get('AWS_S3_BUCKET_REGION'),
        aws_s3_bucket_name=app.conf.get('AWS_S3_BUCKET_NAME'),
    )
    file_name = S3HandlerConstants.PICTURE_FILE_NAME.value.format(
        user_id=db_user_picture.user_id,
        file_extension=file_extension,
    )
    upload_file_response = asyncio.run(
        upload_image_to_s3(
            s3_handler=s3_handler, content_type=content_type, file_obj=image, file_name=file_name,
        )
    )
    engine = create_engine(
        database_url=app.conf.get('POSTGRES_DATABASE_URL'),
        echo=app.conf.get('API_SQLALCHEMY_ECHO'),
        future=app.conf.get('API_SQLALCHEMY_FUTURE'),
    )
    db_session = create_db_session(engine=engine)
    result = asyncio.run(save_uploaded_image_data(db_session, db_user_picture, upload_file_response))
    return result
