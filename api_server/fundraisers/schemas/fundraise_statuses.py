from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from common.constants.fundraisers import FundraiseStatusSchemaConstants


class FundraiseStatusBaseSchema(BaseModel):
    """FundraiseStatus Base schema for FundraiseStatus model."""

    name: str = Field(
        description='Name of a fundraise status.',
        min_length=FundraiseStatusSchemaConstants.CHAR_SIZE_2.value,
        max_length=FundraiseStatusSchemaConstants.CHAR_SIZE_256.value,
    )

    class Config:
        orm_mode = True


class FundraiseStatusOutputSchema(FundraiseStatusBaseSchema):
    """FundraiseStatus Output schema for FundraiseStatus model."""

    id: UUID = Field(description='Unique identifier of a fundraise status.')
    created_at: datetime


class FundraiseStatusInputSchema(FundraiseStatusBaseSchema):
    """FundraiseStatus Input schema for FundraiseStatus model."""
    pass
