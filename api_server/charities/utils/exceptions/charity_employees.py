from fastapi import HTTPException, Request

from starlette.responses import JSONResponse

from common.schemas.responses import ResponseBaseSchema


class CharityEmployeePermissionError(HTTPException):
    """Custom Charity Employee permission error."""
    pass


class CharityEmployeeNotFoundError(HTTPException):
    """Custom Charity Employee not found error."""
    pass


class CharityEmployeeDuplicateError(HTTPException):
    """Custom Employee already added to Charity error."""
    pass


class CharityNonRemovableEmployeeError(HTTPException):
    """Custom Charity non removable Employee error."""
    pass


def charity_employee_permission_error_handler(request: Request, exc: CharityEmployeePermissionError):
    """Handler for CharityEmployeePermissionError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised CharityEmployeePermissionError.

    Returns:
    http response for raised CharityEmployeePermissionError.
    """
    response = ResponseBaseSchema(
        status_code=exc.status_code,
        data=[],
        errors=[{"detail": exc.detail}],
    ).dict()
    return JSONResponse(
        status_code=exc.status_code,
        content=response,
    )


def charity_employee_not_found_error_handler(request: Request, exc: CharityEmployeeNotFoundError):
    """Handler for CharityEmployeeNotFoundError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised CharityEmployeeNotFoundError.

    Returns:
    http response for raised CharityEmployeeNotFoundError.
    """
    response = ResponseBaseSchema(
        status_code=exc.status_code,
        data=[],
        errors=[{"detail": exc.detail}],
    ).dict()
    return JSONResponse(
        status_code=exc.status_code,
        content=response,
    )


def employee_already_added_to_charity_error_handler(request: Request, exc: CharityEmployeeDuplicateError):
    """Handler for CharityEmployeeDuplicateError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised CharityEmployeeDuplicateError.

    Returns:
    http response for raised CharityEmployeeDuplicateError.
    """
    response = ResponseBaseSchema(
        status_code=exc.status_code,
        data=[],
        errors=[{"detail": exc.detail}],
    ).dict()
    return JSONResponse(
        status_code=exc.status_code,
        content=response,
    )


def charity_non_removable_employee_error_handler(request: Request, exc: CharityNonRemovableEmployeeError):
    """Handler for CharityNonRemovableEmployeeError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised CharityNonRemovableEmployeeError.

    Returns:
    http response for raised CharityNonRemovableEmployeeError.
    """
    response = ResponseBaseSchema(
        status_code=exc.status_code,
        data=[],
        errors=[{"detail": exc.detail}],
    ).dict()
    return JSONResponse(
        status_code=exc.status_code,
        content=response,
    )
