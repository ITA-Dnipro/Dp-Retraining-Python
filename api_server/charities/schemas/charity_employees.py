from uuid import UUID

from pydantic import BaseModel, Field

from charities.schemas.employee_roles import EmployeeRoleOutputSchema
from common.constants.charities import EmployeeRoleSchemaConstants
from common.constants.users import UserSchemaConstants
from users.schemas import UserOutputSchema


class EmployeeBaseSchema(BaseModel):
    """Employee Base schema for Employee model."""

    class Config:
        orm_mode = True


class EmployeeDBSchema(EmployeeBaseSchema):
    """Employee Database schema for Employee model."""

    user_id: UUID = Field(description='Unique identifier of a user.')


class EmployeeInputSchema(EmployeeBaseSchema):
    """Employee Input schema for Employee model."""

    user_email: str = Field(
        description='Email address of a user.',
        min_length=UserSchemaConstants.CHAR_SIZE_3.value,
        max_length=UserSchemaConstants.CHAR_SIZE_256.value,
        regex=UserSchemaConstants.EMAIL_REGEX.value,
    )
    role: str = Field(
        description='Name of employee role in charity.',
        min_length=EmployeeRoleSchemaConstants.CHAR_SIZE_2.value,
        max_length=EmployeeRoleSchemaConstants.CHAR_SIZE_256.value,
    )


class EmployeeOutputSchema(EmployeeBaseSchema):
    """Employee Output schema for Employee model."""
    id: UUID = Field(description='Unique identifier of a employee.')
    user: UserOutputSchema
    roles: list[EmployeeRoleOutputSchema]
