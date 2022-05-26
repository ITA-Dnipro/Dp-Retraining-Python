from uuid import UUID

from pydantic import BaseModel, Field

from common.constants.auth import ChangePasswordTokenSchemaConstants


class ChangePasswordTokenBaseSchema(BaseModel):
    """ChangePasswordToken Base Schema."""

    class Config:
        orm_mode = True


class ChangePasswordTokenInputSchema(ChangePasswordTokenBaseSchema):
    """ChangePasswordToken Input Schema."""

    email: str = Field(
        description='Email address of a user.',
        min_length=ChangePasswordTokenSchemaConstants.CHAR_SIZE_3.value,
        max_length=ChangePasswordTokenSchemaConstants.CHAR_SIZE_256.value,
        regex=ChangePasswordTokenSchemaConstants.EMAIL_REGEX.value,
    )


class ChangePasswordTokenOutputSchema(ChangePasswordTokenBaseSchema):
    """ChangePasswordToken Output Schema."""

    id: UUID = Field(description='Unique identifier of a ChangePasswordToken object.')
    token: str = Field(
        description='JWT token of ChangePasswordToken object.',
        max_length=ChangePasswordTokenSchemaConstants.CHAR_SIZE_2048.value,
    )
