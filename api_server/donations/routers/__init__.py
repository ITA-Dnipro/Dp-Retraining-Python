from uuid import UUID

from fastapi import APIRouter, Depends, status

from common.schemas.responses import ResponseBaseSchema
from donations.schemas import DonationInputSchema, DonationOutputSchema
from donations.services import DonationService

donations_router = APIRouter(prefix='/donations', tags=['Donation'])


@donations_router.post('/', response_model=ResponseBaseSchema)
async def donation(donation: DonationInputSchema, donation_service: DonationService = Depends()) -> ResponseBaseSchema:
    """POST '/donations/' endpoint view function.

    Args:
        donation: object that contains info about donation.
        donation_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with DonationOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=DonationOutputSchema.from_orm(await donation_service.add_donation(donation)),
        errors=[],
    )


@donations_router.get('/', response_model=ResponseBaseSchema)
async def get_donations(donation_service: DonationService = Depends()) -> ResponseBaseSchema:
    """GET '/donations/' endpoint view function.

    Args:
        donation_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with list of DonationOutputSchema objects as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=[DonationOutputSchema.from_orm(donation) for donation in await donation_service.get_donations()],
        errors=[],
    )


@donations_router.get('/{id}', response_model=ResponseBaseSchema)
async def get_donation(id: UUID, donation_service: DonationService = Depends()) -> ResponseBaseSchema:
    """GET '/donations/{id}' endpoint view function.

    Args:
        id: UUID of donation.
        donation_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with DonationOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=DonationOutputSchema.from_orm(await donation_service.get_donation_by_id(id_=id)),
        errors=[],
    )
