from common.constants.users import UserSchemaConstants
from pydantic import BaseModel, Field


class AuthUserBaseSchema(BaseModel):
    """Auth User Base Schema."""

    username: str = Field(
        description='Username of a user.',
        min_length=UserSchemaConstants.CHAR_SIZE_2.value,
        max_length=UserSchemaConstants.CHAR_SIZE_64.value,
    )
    password: str = Field(
        description='Password of a user.',
        min_length=UserSchemaConstants.CHAR_SIZE_6.value,
        max_length=UserSchemaConstants.CHAR_SIZE_64.value,
    )

    class Config:
        orm_mode = True


class AuthUserInputSchema(AuthUserBaseSchema):
    """Auth User Input Schema."""
    pass


class AuthUserOutputSchema(BaseModel):
    """Auth User Output Schema."""
    access_token: str
    refresh_token: str


class AuthUserLogoutSchema(BaseModel):
    """Auth User Logout Schema."""
    message: str
