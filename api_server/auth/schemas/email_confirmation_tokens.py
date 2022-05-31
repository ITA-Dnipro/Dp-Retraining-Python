from uuid import UUID

from pydantic import BaseModel, Field

from common.constants.auth import EmailConfirmationTokenSchemaConstants


class EmailConfirmationTokenBaseSchema(BaseModel):
    """EmailConfirmationToken Base Schema."""

    class Config:
        orm_mode = True


class EmailConfirmationTokenInputSchema(EmailConfirmationTokenBaseSchema):
    """EmailConfirmationToken Input Schema."""

    email: str = Field(
        description='Email address of a user.',
        min_length=EmailConfirmationTokenSchemaConstants.CHAR_SIZE_3.value,
        max_length=EmailConfirmationTokenSchemaConstants.CHAR_SIZE_256.value,
        regex=EmailConfirmationTokenSchemaConstants.EMAIL_REGEX.value,
    )


class EmailConfirmationTokenOutputSchema(EmailConfirmationTokenBaseSchema):
    """EmailConfirmationToken Output Schema."""

    id: UUID = Field(description='Unique identifier of a EmailConfirmationToken object.')
    token: str = Field(
        description='JWT token of EmailConfirmationToken object.',
        max_length=EmailConfirmationTokenSchemaConstants.CHAR_SIZE_2048.value,
    )


class EmailConfirmationTokenSuccessSchema(BaseModel):
    """EmailConfirmationToken Success Schema."""
    message: str = Field(
        description='A message with succesfull user activation.',
    )
