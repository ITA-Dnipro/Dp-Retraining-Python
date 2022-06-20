from uuid import UUID

from pydantic import BaseModel, Field

from charities.schemas.employee_roles import EmployeeRoleOutputSchema
from users.schemas import UserOutputSchema


class EmployeeBaseSchema(BaseModel):
    """Employee Base schema for Employee model."""

    class Config:
        orm_mode = True


class EmployeeInputSchema(EmployeeBaseSchema):
    """Employee Input schema for Employee model."""

    user_id: UUID = Field(description='Unique identifier of a user.')


class EmployeeOutputSchema(EmployeeBaseSchema):
    """Employee Output schema for Employee model."""
    id: UUID = Field(description='Unique identifier of a employee.')
    user: UserOutputSchema
    roles: list[EmployeeRoleOutputSchema]
