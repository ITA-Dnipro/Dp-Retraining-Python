from uuid import UUID

from pydantic import BaseModel, Field

from common.constants.charities import EmployeeRoleSchemaConstants


class EmployeeRoleBaseSchema(BaseModel):
    """EmployeeRole Base schema for EmployeeRole model."""

    name: str = Field(
        description='Name of a employee role.',
        min_length=EmployeeRoleSchemaConstants.CHAR_SIZE_2.value,
        max_length=EmployeeRoleSchemaConstants.CHAR_SIZE_256.value,
    )

    class Config:
        orm_mode = True


class EmployeeRoleInputSchema(EmployeeRoleBaseSchema):
    """EmployeeRole Input schema for EmployeeRole model."""
    pass


class EmployeeRoleOutputSchema(EmployeeRoleBaseSchema):
    """EmployeeRole Output schema for EmployeeRole model."""

    id: UUID = Field(description='Unique identifier of a employee role.')


class EmployeeRoleOutputMessageSchema(BaseModel):
    """EmployeeRole Output Message schema for EmployeeRole model."""

    message: str = Field(description='Message in regard of employee role.')
