from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from common.constants.users import UserSchemaConstants


class UserBaseSchema(BaseModel):
    """User Base schema for User model."""

    first_name: Optional[str] = Field(
        description='First name of a user.',
        min_length=UserSchemaConstants.CHAR_SIZE_2.value,
        max_length=UserSchemaConstants.CHAR_SIZE_64.value,
    )
    last_name: Optional[str] = Field(
        description='Last name of a user.',
        min_length=UserSchemaConstants.CHAR_SIZE_2.value,
        max_length=UserSchemaConstants.CHAR_SIZE_64.value,
    )
    username: str = Field(
        description='Username of a user.',
        min_length=UserSchemaConstants.CHAR_SIZE_2.value,
        max_length=UserSchemaConstants.CHAR_SIZE_64.value,
    )
    email: str = Field(
        description='Email address of a user.',
        min_length=UserSchemaConstants.СHAR_SIZE_3.value,
        max_length=UserSchemaConstants.CHAR_SIZE_256.value,
        regex=UserSchemaConstants.EMAIL_REGEX.value,
    )
    phone_number: str = Field(
        description='Password of a user.',
        min_length=UserSchemaConstants.СHAR_SIZE_3.value,
        max_length=UserSchemaConstants.CHAR_SIZE_64.value,
    )

    class Config:
        orm_mode = True


class UserInputSchema(UserBaseSchema):
    """User Input schema for User model."""
    password: str = Field(
        description='Password of a user.',
        min_length=UserSchemaConstants.CHAR_SIZE_6.value,
        max_length=UserSchemaConstants.CHAR_SIZE_64.value,
    )


class UserOutputSchema(UserBaseSchema):
    """User Output schema for User model."""
    id: UUID = Field(description='Unique identifier of a user.')
    is_active: bool = Field(description='Boolean field whether a user is active or not.')
    created_at: datetime = Field(description="Datetime of user's creation.")
