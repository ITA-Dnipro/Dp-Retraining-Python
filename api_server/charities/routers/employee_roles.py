from uuid import UUID

from fastapi import APIRouter, Depends, status

from charities.schemas import EmployeeRoleOutputSchema
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
    ResponseBaseSchema object with EmployeeRoleOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=[
            EmployeeRoleOutputSchema.from_orm(role) for role in
            await employee_roles_service.get_employee_roles(charity_id, employee_id)
        ],
        errors=[],
    )
