from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, condecimal

from common.constants.fundraisers import FundraiseSchemaConstants


class FundraiseBaseSchema(BaseModel):
    """Fundraise Base schema for Fundraise model."""

    title: str = Field(
        description='Title of a fundraise.',
        min_length=FundraiseSchemaConstants.CHAR_SIZE_2.value,
        max_length=FundraiseSchemaConstants.CHAR_SIZE_512.value,
    )
    description: str = Field(
        description='Description of a fundraise.',
        min_length=FundraiseSchemaConstants.CHAR_SIZE_2.value,
        max_length=FundraiseSchemaConstants.CHAR_SIZE_8192.value,
    )
    goal: condecimal(
        gt=FundraiseSchemaConstants.MIN_VALUE.value,
        max_digits=FundraiseSchemaConstants.NUM_PRECISION.value,
        decimal_places=FundraiseSchemaConstants.NUM_SCALE.value,
    )
    ending_at: datetime = None

    class Config:
        orm_mode = True


class FundraiseOutputSchema(FundraiseBaseSchema):
    """Fundraise Output schema for Fundraise model."""
    id: UUID = Field(description='Unique identifier of a fundraise.')


class FundraiseFullOutputSchema(FundraiseOutputSchema):
    """Fundraise Output schema with all nested schemas included."""
    charity: CharityOutputSchema


class FundraisePaginatedOutputSchema(BaseModel):
    """Fundraise paginated output schema for Fundraise model."""
    current_page: int
    has_next: bool
    has_previous: bool
    items: list[FundraiseFullOutputSchema]
    next_page: int | None
    previous_page: int | None
    total_pages: int

    class Config:
        orm_mode = True


from charity.schemas import CharityOutputSchema  # noqa

FundraiseFullOutputSchema.update_forward_refs()
