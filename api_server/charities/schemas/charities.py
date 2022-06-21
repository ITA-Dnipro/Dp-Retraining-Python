from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, root_validator

from common.constants.charities import CharitySchemaConstants
from common.exceptions.schemas import SchemaExceptionMsgs


class CharityBaseSchema(BaseModel):
    """Charity Base Schema for Charity model."""
    title: str = Field(
        description='Title of a charity.',
        min_length=CharitySchemaConstants.CHAR_SIZE_2.value,
        max_length=CharitySchemaConstants.CHAR_SIZE_512.value,
    )
    description: str = Field(
        description='Description of a charity.',
        min_length=CharitySchemaConstants.CHAR_SIZE_2.value,
        max_length=CharitySchemaConstants.CHAR_SIZE_8192.value,
    )
    phone_number: str = Field(
        description='Phone number of a charity.',
        min_length=CharitySchemaConstants.CHAR_SIZE_2.value,
        max_length=CharitySchemaConstants.CHAR_SIZE_128.value,
    )
    email: str = Field(
        description='Email of a charity.',
        regex=CharitySchemaConstants.EMAIL_REGEX.value,
        min_length=CharitySchemaConstants.CHAR_SIZE_2.value,
        max_length=CharitySchemaConstants.CHAR_SIZE_256.value,
    )

    class Config:
        orm_mode = True


class CharityOutputSchema(CharityBaseSchema):
    """Charity Output Schema for Charity model."""
    id: UUID = Field(description='Unique identifier of a charity.')


class CharityFullOutputSchema(CharityOutputSchema):
    """Charity Output schema with all nested schemas included."""
    fundraisers: List[Optional['FundraiseOutputSchema']]
    employees: list[EmployeeOutputSchema]


class CharityInputSchema(CharityBaseSchema):
    """Charity Input Schema for Charity model."""
    pass


class CharityUpdateSchema(BaseModel):
    """Charity Update Schema for Charity model."""
    title: Optional[str] = Field(
        description='Title of a charity.',
        min_length=CharitySchemaConstants.CHAR_SIZE_2.value,
        max_length=CharitySchemaConstants.CHAR_SIZE_512.value,
    )
    description: Optional[str] = Field(
        description='Description of a charity.',
        min_length=CharitySchemaConstants.CHAR_SIZE_2.value,
        max_length=CharitySchemaConstants.CHAR_SIZE_8192.value,
        exclude=False
    )
    phone_number: Optional[str] = Field(
        description='Phone number of a charity.',
        min_length=CharitySchemaConstants.CHAR_SIZE_2.value,
        max_length=CharitySchemaConstants.CHAR_SIZE_128.value,
    )
    email: Optional[str] = Field(
        description='Email of a charity.',
        regex=CharitySchemaConstants.EMAIL_REGEX.value,
        min_length=CharitySchemaConstants.CHAR_SIZE_2.value,
        max_length=CharitySchemaConstants.CHAR_SIZE_256.value,
    )

    @root_validator
    def exclude_none_values(cls, incoming_data: dict) -> dict:
        """Excludes field from schema if value is None.

        Args:
            incoming_data: Schema incoming data.

        Returns:
        dict with incoming_data.
        """
        incoming_data = {k: v for k, v in incoming_data.items() if v}
        return incoming_data

    @root_validator
    def at_least_one_field_present(cls, incoming_data: dict) -> dict:
        """Checks if at least one field in schema present.

        Args:
            incoming_data: Schema incoming data.

        Returns:
        dict with incoming_data.
        """
        if not any(incoming_data.values()):
            raise ValueError(SchemaExceptionMsgs.AT_LEAST_ONE_FIELD_PRESENT.value)
        return incoming_data

    class Config:
        orm_mode = True


class AddManagerSchema(BaseModel):
    user_id: UUID
    is_supermanager: bool


class ManagerResponseSchema(BaseModel):
    is_supermanager: bool
    # user: UserOutputSchema

    class Config:
        orm_mode = True


class CharityPaginatedOutputSchema(BaseModel):
    """Charity paginated output schema for Charity model."""
    current_page: int
    has_next: bool
    has_previous: bool
    items: list[CharityOutputSchema]
    next_page: int | None
    previous_page: int | None
    total_pages: int

    class Config:
        orm_mode = True


from charities.schemas.employees import EmployeeOutputSchema  # noqa
from fundraisers.schemas import FundraiseOutputSchema  # noqa

CharityFullOutputSchema.update_forward_refs()
