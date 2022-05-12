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
