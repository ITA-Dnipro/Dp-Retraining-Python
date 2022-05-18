import re

from common.exceptions.db import SqlalchemyExceptionConstants
from common.schemas.responses import ResponseBaseSchema
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


def parse_integrity_error(exc: IntegrityError) -> tuple:
    """Get sqlalchemy IntegrityError and parse it to get data from the error.
    Args:
        exc: raised sqlalchemy IntegrityError.
    Returns:
    tuple with data: table_name, field where error occurred and value of that field.
    """
    table_name = re.search(
        SqlalchemyExceptionConstants.INTEGRITY_ERROR_TABLE_NAME_REGEX.value,
        exc.orig.args[0],
    ).group(1)
    table_name = table_name.split('_')[0][:-1].capitalize()
    field, value = re.findall(
        SqlalchemyExceptionConstants.INTEGRITY_ERROR_FIELD_VALUE_REGEX.value,
        exc.orig.args[0],
    )
    return table_name, field, value


def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Handler for IntegrityError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised IntegrityError.

    Returns:
    http response for raised IntegrityError.
    """
    ERROR_MESSAGE = get_error_message(exc)
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    response = ResponseBaseSchema(
        status_code=STATUS_CODE,
        data=[],
        errors=[{'detail': ERROR_MESSAGE}],
    ).dict()
    return JSONResponse(status_code=STATUS_CODE, content=response)


def get_error_message(exc: IntegrityError) -> str:
    """Get formatted error message bases of error.orig type.
    Args:
        exc: raised sqlalchemy IntegrityError.
    Returns:
    Properly formatted error message.
    """
    table_name, field, value = parse_integrity_error(exc=exc)
    SQLALCHEMY_INTEGRITY_ERROR_MAP = {
        'IntegrityError': f"{table_name} with {field}: '{value}' already exists."
    }
    return SQLALCHEMY_INTEGRITY_ERROR_MAP[exc.orig.__class__.__name__]
