from uuid import UUID

from fastapi import APIRouter, Depends, status

from fastapi_jwt_auth import AuthJWT

from charities.schemas import EmployeeRoleInputSchema, EmployeeRoleOutputMessageSchema, EmployeeRoleOutputSchema
from charities.services import EmployeeRoleService
from common.schemas.responses import ResponseBaseSchema

employee_roles_router = APIRouter(prefix='/roles', tags=['Employee-roles'])


@employee_roles_router.get('/', response_model=ResponseBaseSchema)
async def get_employee_roles(
        charity_id: UUID,
        employee_id: UUID,
        employee_roles_service: EmployeeRoleService = Depends(),
):
    """GET '/charities/{charity_id}/employees/{employee_id}/roles' endpoint view function.

    Args:
        charity_id: UUID of charity.
        employee_id: UUID of employee.
        employee_roles_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with list of EmployeeRoleOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=[
            EmployeeRoleOutputSchema.from_orm(role) for role in
            await employee_roles_service.get_employee_roles(charity_id, employee_id)
        ],
        errors=[],
    )


@employee_roles_router.get('/{role_id}', response_model=ResponseBaseSchema)
async def get_employee_role(
        charity_id: UUID,
        employee_id: UUID,
        role_id: UUID,
        employee_roles_service: EmployeeRoleService = Depends(),
):
    """GET '/charities/{charity_id}/employees/{employee_id}/roles/{role_id}' endpoint view function.

    Args:
        charity_id: UUID of charity.
        employee_id: UUID of employee.
        role_id: UUID of EmployeeRole.
        employee_roles_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with EmployeeRoleOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=EmployeeRoleOutputSchema.from_orm(
            await employee_roles_service.get_employee_role_by_id(charity_id, employee_id, role_id)
        ),
        errors=[],
    )


@employee_roles_router.post('/', response_model=ResponseBaseSchema)
async def post_employee_roles(
        charity_id: UUID,
        employee_id: UUID,
        role_data: EmployeeRoleInputSchema,
        employee_roles_service: EmployeeRoleService = Depends(),
        Authorize: AuthJWT = Depends(),
):
    """POST '/charities/{charity_id}/employees/{employee_id}/roles' endpoint view function.

    Args:
        charity_id: UUID of charity.
        employee_id: UUID of employee.
        role_data: Serialized EmployeeRoleInputSchema object.
        employee_roles_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with EmployeeRoleOutputSchema object as response data.
    """
    Authorize.jwt_required()
    jwt_subject = Authorize.get_jwt_subject()

    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=EmployeeRoleOutputSchema.from_orm(
            await employee_roles_service.add_role_to_employee(charity_id, employee_id, jwt_subject, role_data)
        ),
        errors=[],
    )


@employee_roles_router.delete('/{role_id}', response_model=ResponseBaseSchema)
async def delete_employee_role(
        charity_id: UUID,
        employee_id: UUID,
        role_id: UUID,
        employee_roles_service: EmployeeRoleService = Depends(),
        Authorize: AuthJWT = Depends(),
):
    """DELETE '/charities/{charity_id}/employees/{employee_id}/roles/{role_id}' endpoint view function.

    Args:
        charity_id: UUID of charity.
        employee_id: UUID of employee.
        role_id: UUID of EmployeeRole.
        employee_roles_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with EmployeeRoleOutputMessageSchema object as response data.
    """
    Authorize.jwt_required()
    jwt_subject = Authorize.get_jwt_subject()

    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=EmployeeRoleOutputMessageSchema(
            **await employee_roles_service.remove_role_from_employee(charity_id, employee_id, role_id, jwt_subject)
        ),
        errors=[],
    )
