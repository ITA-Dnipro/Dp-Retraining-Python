from typing import Type

from fastapi import Form, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from pydantic import BaseModel, ValidationError


def form_json_deserializer(schema: Type[BaseModel], data: str = Form(...)) -> Type[BaseModel]:
    """Helper to serialize request data not automatically included in an application/json body but
    within somewhere else like a form parameter. This makes an assumption that the form
    parameter with JSON data is called 'data'.
    Source: https://stackoverflow.com/questions/65504438/how-to-add-both-file-and-json-body-in-a-fastapi-post-request

    Args:
        schema: Pydantic model to serialize into.
        data: raw str data representing the Pydantic model.
    Raises:
        ValidationError: if there are errors parsing the given 'data' into the given 'schema'.

    Returns:
    Serialized data from schema.
    """
    try:
        return schema.parse_raw(data)
    except ValidationError as e:
        raise HTTPException(detail=jsonable_encoder(e.errors()), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
