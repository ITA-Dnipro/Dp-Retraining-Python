from uuid import UUID

from fastapi import APIRouter, Depends, status

from charities.schemas import EmployeeInputSchema
from charities.services import CharityEmployeeService
from common.schemas.responses import ResponseBaseSchema
from users.schemas import UserOutputSchema

charity_employees_router = APIRouter(prefix='/employees', tags=['Charity-employees'])


@charity_employees_router.post(
    '/', response_model=ResponseBaseSchema, status_code=status.HTTP_201_CREATED,
)
async def add_employee_to_charity(
        charity_id: UUID,
        employee_data: EmployeeInputSchema,
        charity_employee_service: CharityEmployeeService = Depends(),
):
    """POST '/charities/{id}/employees' endpoint view function.

    Args:
        charity_id: UUID of charity.
        employee_data: AddManagerData object.
        charity_employee_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with EmployeeOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_201_CREATED,
        data=UserOutputSchema.from_orm(
            await charity_employee_service.add_employee_to_charity(charity_id, employee_data)
        ),
        errors=[],
    )
