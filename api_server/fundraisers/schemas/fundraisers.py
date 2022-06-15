from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, condecimal
from sqlalchemy.ext.associationproxy import _AssociationList

from common.constants.fundraisers import FundraiseSchemaConstants
from common.exceptions.schemas import SchemaExceptionMsgs


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
    ending_at: datetime | None = None

    class Config:
        orm_mode = True


class FundraiseOutputSchema(FundraiseBaseSchema):
    """Fundraise Output schema for Fundraise model."""
    id: UUID = Field(description='Unique identifier of a fundraise.')


class FundraiseFullOutputSchema(FundraiseOutputSchema):
    """Fundraise Output schema with all nested schemas included."""
    charity: CharityOutputSchema
    statuses: FundraiseStatusOutputAssociationListSchema


class FundraiseStatusOutputAssociationListSchema(_AssociationList):
    """Custom FundraiseStatusOutput schema for sqlalchemy association_proxy field."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, association_list: _AssociationList) -> list[FundraiseStatusOutputSchema]:
        """Custom validator checks if field is sqlalchemy _AssociationList object and serializing it with
        UserOutputSchema.

        Args:
            association_list: sqlalchemy _AssociationList object.

        Returns:
        list of FundraiseStatusOutputSchema objects.
        """
        if not isinstance(association_list, _AssociationList):
            raise TypeError(SchemaExceptionMsgs.INVALID_ASSOCIATION_LIST_TYPE.value)
        return [FundraiseStatusOutputSchema.from_orm(obj) for obj in association_list]


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


class FundraiseInputSchema(FundraiseBaseSchema):
    """Fundraise Input schema for Fundraise model."""
    charity_id: UUID = Field(description='Unique identifier of a charity.')


class FundraiseUpdateSchema(FundraiseBaseSchema):
    """Fundraise Update schema for Fundraise model."""
    pass


from charity.schemas import CharityOutputSchema  # noqa
from fundraisers.schemas import FundraiseStatusOutputSchema  # noqa

FundraiseFullOutputSchema.update_forward_refs()
