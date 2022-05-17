from uuid import UUID

from fastapi import APIRouter, Depends, status

from common.schemas.responses import ResponseBaseSchema
from refills.schemas import RefillInputSchema, RefillOutputSchema
from refills.services import RefillService

refills_router = APIRouter(prefix='/refills', tags=['Refill'])


@refills_router.post('/', response_model=ResponseBaseSchema)
async def refill(refill: RefillInputSchema, refill_service: RefillService = Depends()) -> ResponseBaseSchema:
    """POST '/refills/' endpoint view function.

    Args:
        refill: object that contains info about refill.
        refill_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with RefillOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=RefillOutputSchema.from_orm(await refill_service.add_refill(refill)),
        errors=[],
    )


@refills_router.get('/', response_model=ResponseBaseSchema)
async def get_refills(refill_service: RefillService = Depends()) -> ResponseBaseSchema:
    """GET '/refills/' endpoint view function.

    Args:
        refill_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with list of RefillOutputSchema objects as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=[RefillOutputSchema.from_orm(refill) for refill in await refill_service.get_refills()],
        errors=[],
    )


@refills_router.get('/{id}', response_model=ResponseBaseSchema)
async def get_refill(id: UUID, refill_service: RefillService = Depends()) -> ResponseBaseSchema:
    """GET '/refills/{id}' endpoint view function.

    Args:
        id: UUID of refill.
        refill_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with RefillOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=RefillOutputSchema.from_orm(await refill_service.get_refill_by_id(id_=id)),
        errors=[],
    )
