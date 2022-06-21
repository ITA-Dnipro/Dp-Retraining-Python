from fastapi import HTTPException, Request

from starlette.responses import JSONResponse

from common.schemas.responses import ResponseBaseSchema


class CharityNotFoundError(HTTPException):
    """Custom Fundraise not found error."""
    pass


class CharityEmployeePermissionError(HTTPException):
    """Custom Charity employee permission error."""
    pass


class CharityEmployeeRolePermissionError(HTTPException):
    """Custom Charity employee permission error."""
    pass


def charity_not_found_error_handler(request: Request, exc: CharityNotFoundError):
    """Handler for CharityNotFoundError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised CharityNotFoundError.

    Returns:
    http response for raised CharityNotFoundError.
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


def charity_employee_role_permission_error_handler(request: Request, exc: CharityEmployeeRolePermissionError):
    """Handler for CharityEmployeeRolePermissionError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised CharityEmployeeRolePermissionError.

    Returns:
    http response for raised CharityEmployeeRolePermissionError.
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
