from uuid import UUID

from pydantic import BaseModel, Field

from common.constants.auth import ChangePasswordTokenSchemaConstants
from common.constants.users import UserSchemaConstants


class ForgetPasswordBaseSchema(BaseModel):
    """ForgetPassword Base Schema."""

    class Config:
        orm_mode = True


class ForgetPasswordInputSchema(ForgetPasswordBaseSchema):
    """ForgetPassword Input Schema."""

    email: str = Field(
        description='Email address of a user.',
        min_length=ChangePasswordTokenSchemaConstants.CHAR_SIZE_3.value,
        max_length=ChangePasswordTokenSchemaConstants.CHAR_SIZE_256.value,
        regex=ChangePasswordTokenSchemaConstants.EMAIL_REGEX.value,
    )


class ForgetPasswordOutputSchema(ForgetPasswordBaseSchema):
    """ForgetPassword Output Schema."""

    id: UUID = Field(description='Unique identifier of a ChangePasswordToken object.')
    token: str = Field(
        description='JWT token of ChangePasswordToken object.',
        max_length=ChangePasswordTokenSchemaConstants.CHAR_SIZE_2048.value,
    )


class ChangePasswordBaseSchema(BaseModel):
    """ChangePassword Base Schema."""

    class Config:
        orm_mode = True


class ChangePasswordInputSchema(ChangePasswordBaseSchema):
    """ChangePassword Input Schema."""
    token: str = Field(
        description='JWT token of ChangePasswordToken object.',
        max_length=ChangePasswordTokenSchemaConstants.CHAR_SIZE_2048.value,
    )
    password: str = Field(
        description='Password of a user.',
        min_length=UserSchemaConstants.CHAR_SIZE_6.value,
        max_length=UserSchemaConstants.CHAR_SIZE_64.value,
    )


class ChangePasswordOutputSchema(ForgetPasswordBaseSchema):
    """ChangePassword Output Schema."""
    message: str = Field(
        description="A user's successful password change message.",
    )
