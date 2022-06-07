from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from common.constants.user_pictures import UserPictureSchemaConstants


class UserPictureBaseSchema(BaseModel):
    """UserPictureBase schema for UserPicture model."""

    class Config:
        orm_mode = True


class UserPictureOutputSchema(UserPictureBaseSchema):
    """UserPictureOutput for UserPicture model."""
    id: UUID = Field(description="Unique identifier of a user's picture.")
    url: str | None = Field(
        description="url of user's picture.",
        min_length=UserPictureSchemaConstants.CHAR_SIZE_2.value,
        max_length=UserPictureSchemaConstants.CHAR_SIZE_512.value,
    )


class UserPictureUpdateSchema(UserPictureBaseSchema):
    """UserPictureOutput for UserPicture model."""
    url: str = Field(
        description="url of user's picture.",
        min_length=UserPictureSchemaConstants.CHAR_SIZE_2.value,
        max_length=UserPictureSchemaConstants.CHAR_SIZE_512.value,
    )
    updated_at: datetime = Field(
        description="updated time of user's picture.",
    )
    etag: str = Field(
        description='Etag of user picture in AWS S3 bucket.',
    )
