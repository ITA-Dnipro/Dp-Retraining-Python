from uuid import UUID

from pydantic import BaseModel, Field


class BalanceBaseSchema(BaseModel):
    """Balance Base schema for Balance model."""

    amount: float = Field(
        min_value=0,
        max_value=100_000_000
    )

    class Config:
        orm_mode = True


class BalanceOutputSchema(BalanceBaseSchema):
    """Balance Output schema for balance model."""
    id: UUID = Field(description='Unique identifier of a balance.')
    amount: float = Field(description='Numeric field with amount of funds in the account.')


class BalanceUpdateSchema(BalanceBaseSchema):
    """Balance Update schema for Balance model."""
    pass
