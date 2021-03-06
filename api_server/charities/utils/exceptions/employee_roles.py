from fastapi import HTTPException, Request

from starlette.responses import JSONResponse

from common.schemas.responses import ResponseBaseSchema


class EmployeeRoleNotSupportedError(HTTPException):
    """Custom Employee role not supported error."""
    pass


class CharityEmployeeRoleDuplicateError(HTTPException):
    """Custom EmployeeRole already added to charity employee error."""
    pass


class CharityEmployeeRolePermissionError(HTTPException):
    """Custom Charity employee role permission error."""
    pass


class EmployeeRoleNotFoundError(HTTPException):
    """Custom Employee role not found error."""
    pass


class EmployeeNonRemovableEmployeeRoleError(HTTPException):
    """Custom Employee non removable EmployeeRole error."""
    pass


def employee_role_not_supported_error_handler(request: Request, exc: EmployeeRoleNotSupportedError):
    """Handler for EmployeeRoleNotSupportedError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised EmployeeRoleNotSupportedError.

    Returns:
    http response for raised EmployeeRoleNotSupportedError.
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


def employee_role_already_added_to_employee_error_handler(request: Request, exc: CharityEmployeeRoleDuplicateError):
    """Handler for CharityEmployeeRoleDuplicateError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised CharityEmployeeRoleDuplicateError.

    Returns:
    http response for raised CharityEmployeeRoleDuplicateError.
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


def employee_role_not_found_error_handler(request: Request, exc: EmployeeRoleNotFoundError):
    """Handler for EmployeeRoleNotFoundError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised EmployeeRoleNotFoundError.

    Returns:
    http response for raised EmployeeRoleNotFoundError.
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


def employee_non_removable_employee_role_error_handler(request: Request, exc: EmployeeNonRemovableEmployeeRoleError):
    """Handler for EmployeeNonRemovableEmployeeRoleError exception that makes http response.

    Args:
        request: FastAPI Request object.
        exc: raised EmployeeNonRemovableEmployeeRoleError.

    Returns:
    http response for raised EmployeeNonRemovableEmployeeRoleError.
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
