from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, condecimal


class RefillBaseSchema(BaseModel):
    """Refill Base schema for Refill model."""

    amount: condecimal(ge=0, decimal_places=2) = Field(
        min_value=0,
        max_value=100_000_000,
    )
    balance_id: UUID = Field(
        description="User's balance id"
    )

    class Config:
        orm_mode = True


class RefillOutputSchema(RefillBaseSchema):
    """Refill Output schema for Refill model."""

    id: UUID = Field(description="Unique identifier of a balance.")
    balance_id: UUID = Field(description="User's balance id")
    amount: condecimal(ge=0, decimal_places=2) = Field(
        description="Numeric field with amount of funds in the account."
    )


class RefillInputSchema(RefillBaseSchema):
    """Refill Input schema for Refill model."""

    balance_id: Optional[UUID] = Field(description="Unique identifier of a balance.")
    amount: condecimal(ge=0, decimal_places=2) = Field(
        description="Numeric field with amount of funds in the account."
    )
