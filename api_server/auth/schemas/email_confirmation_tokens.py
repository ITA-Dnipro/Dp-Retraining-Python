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
