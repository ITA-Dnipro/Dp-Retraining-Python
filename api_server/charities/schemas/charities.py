from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.main import ModelMetaclass
from sqlalchemy.ext.associationproxy import _AssociationList

from common.constants.charities.charities import CharitySchemaConstants
from common.exceptions.schemas import SchemaExceptionMsgs


class AllOptional(ModelMetaclass):
    def __new__(mcs, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        namespaces['__annotations__'] = annotations
        return super().__new__(mcs, name, bases, namespaces, **kwargs)


class CharityDefaultSchema(BaseModel):
    title: str = Field(description='Name of organisation')
    description: str = Field(description='Short description of organisation')
    phone_number: str = Field(
        regex=CharitySchemaConstants.PHONE_REGEX.value,
        description='Phone number must be from Ukrainian operator and same to that template: +380xxxxxxxxx',
    )
    email: str = Field(regex=CharitySchemaConstants.EMAIL_REGEX.value, description='Enter valid email')

    class Config:
        orm_mode = True


class CharityOutputSchema(CharityDefaultSchema):
    """Charity Output Schema."""
    id: UUID = Field(description="id of current organisation")


# class UserOutputAssociationListSchema(_AssociationList):
#     """Custom UserOutput schema for sqlalchemy association_proxy field."""
# 
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
# 
#     @classmethod
#     def validate(cls, association_list: _AssociationList) -> list[UserOutputSchema]:
#         """Custom validator checks if field is sqlalchemy _AssociationList object and serializing it with
#         UserOutputSchema.
# 
#         Args:
#             association_list: sqlalchemy _AssociationList object.
# 
#         Returns:
#         list of UserOutputSchema objects.
#         """
#         if not isinstance(association_list, _AssociationList):
#             raise TypeError(SchemaExceptionMsgs.INVALID_ASSOCIATION_LIST_TYPE.value)
#         return [UserOutputSchema.from_orm(obj.user) for obj in association_list]


class CharityFullOutputSchema(CharityOutputSchema):
    """Charity Output schema with all nested schemas included."""
    fundraisers: List[Optional['FundraiseOutputSchema']]
    employees: list[EmployeeOutputSchema]


class CharityInputSchema(CharityDefaultSchema):
    pass


class CharityUpdateSchema(CharityDefaultSchema, metaclass=AllOptional):
    pass


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

# from users.schemas import UserOutputSchema  # noqa

CharityFullOutputSchema.update_forward_refs()
