from pydantic import BaseModel, Field

from common.constants.users import UserSchemaConstants


class AuthUserBaseSchema(BaseModel):
    """Auth user Base schema."""

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
    pass


class AuthUserOutputSchema(BaseModel):
    access_token: str
    refresh_token: str


class AuthUserLogoutSchema(BaseModel):
    message: str
