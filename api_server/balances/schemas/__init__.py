from uuid import UUID

from pydantic import BaseModel, Field, condecimal


class BalanceBaseSchema(BaseModel):
    """Balance Base schema for Balance model."""

    amount: condecimal(ge=0, decimal_places=2) = Field(
        min_value=0,
        max_value=100_000_000,
    )

    class Config:
        orm_mode = True


class BalanceOutputSchema(BalanceBaseSchema):
    """Balance Output schema for balance model."""

    id: UUID = Field(description="Unique identifier of a balance.")
    amount: condecimal(ge=0, decimal_places=2) = Field(
        description="Numeric field with amount of funds in the account."
    )


class BalanceUpdateSchema(BalanceBaseSchema):
    """Balance Update schema for Balance model."""
    pass


class BalanceInputSchema(BalanceBaseSchema):
    """Balance Input schema for Balance model."""
    pass
