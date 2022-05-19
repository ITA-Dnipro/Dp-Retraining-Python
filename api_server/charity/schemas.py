from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.main import ModelMetaclass

from common.constants.charities import CharitySchemaConstants


class AllOptional(ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        namespaces['__annotations__'] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)


class CharityOutputSchema(BaseModel):
    title: str = Field()
    description: str = Field()
    phone_number: str = Field(regex=CharitySchemaConstants.PHONE_REGEX.value)
    organisation_email: str = Field(regex=CharitySchemaConstants.EMAIL_REGEX.value)

    class Config:
        orm_mode = True


class CharityInputSchema(CharityOutputSchema):
    user_id: UUID = Field()


class CharityUpdateSchema(CharityOutputSchema, metaclass=AllOptional):
    pass
