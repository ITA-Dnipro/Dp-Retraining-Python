from uuid import UUID

from fastapi import APIRouter, Depends, status

from fastapi_jwt_auth import AuthJWT

from charities.schemas import EmployeeInputSchema, EmployeeOutputSchema
from charities.services import CharityEmployeeService
from common.schemas.responses import ResponseBaseSchema

charity_employees_router = APIRouter(prefix='/employees', tags=['Charity-employees'])


@charity_employees_router.post(
    '/', response_model=ResponseBaseSchema, status_code=status.HTTP_201_CREATED,
)
async def post_charity_employees(
        charity_id: UUID,
        employee_data: EmployeeInputSchema,
        charity_employee_service: CharityEmployeeService = Depends(),
        Authorize: AuthJWT = Depends(),
):
    """POST '/charities/{id}/employees' endpoint view function.

    Args:
        charity_id: UUID of charity.
        employee_data: EmployeeInputSchema object.
        charity_employee_service: dependency as business logic instance.
        Authorize: dependency of AuthJWT for JWT tokens.

    Returns:
    ResponseBaseSchema object with EmployeeOutputSchema object as response data.
    """
    Authorize.jwt_required()
    jwt_subject = Authorize.get_jwt_subject()

    return ResponseBaseSchema(
        status_code=status.HTTP_201_CREATED,
        data=EmployeeOutputSchema.from_orm(
            await charity_employee_service.add_employee_to_charity(charity_id, jwt_subject, employee_data)
        ),
        errors=[],
    )


@charity_employees_router.get('/', response_model=ResponseBaseSchema)
async def get_charity_employees(
        charity_id: UUID,
        charity_employee_service: CharityEmployeeService = Depends(),
):
    """GET '/charities/{id}/employees' endpoint view function.

    Args:
        charity_id: UUID of charity.
        charity_employee_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with EmployeeOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=[
            EmployeeOutputSchema.from_orm(employee) for employee in
            await charity_employee_service.get_charity_employees(charity_id)
        ],
        errors=[],
    )
