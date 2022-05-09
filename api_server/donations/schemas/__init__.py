from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, condecimal


class DonationBaseSchema(BaseModel):
    """Donation Base schema for Donation model."""

    amount: condecimal(ge=0, decimal_places=2) = Field(
        min_value=0,
        max_value=100_000_000,
    )
    sender_id: UUID = Field(
        description="sender's balance id"
    )
    recipient_id: UUID = Field(
        description="recipient's balance id"
    )

    class Config:
        orm_mode = True


class DonationOutputSchema(DonationBaseSchema):
    """Donation Output schema for Donation model."""

    id: UUID = Field(description="Unique identifier of a balance.")
    sender_id: UUID = Field(description="sender's balance id")
    recipient_id: UUID = Field(description="recipient's balance id")
    amount: condecimal(ge=0, decimal_places=2) = Field(
        description="Numeric field with amount of funds in the account."
    )


class DonationInputSchema(DonationBaseSchema):
    """Donation Input schema for Donation model."""

    sender_id: Optional[UUID] = Field(description="sender's balance id")
    recipient_id: UUID = Field(description="recipient's balance id")
    amount: condecimal(ge=0, decimal_places=2) = Field(
        description="Numeric field with amount of funds in the account."
    )
