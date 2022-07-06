from uuid import UUID

from fastapi import APIRouter, Depends, status

from fastapi_jwt_auth import AuthJWT

from common.schemas.responses import ResponseBaseSchema
from fundraisers.schemas import FundraiseStatusInputSchema, FundraiseStatusOutputSchema
from fundraisers.services import FundraiseStatusService

fundraise_statuses_router = APIRouter(prefix='/statuses', tags=['Fundraise-statuses'])


@fundraise_statuses_router.get('/', response_model=ResponseBaseSchema)
async def get_fundraise_statuses(
        fundraise_id: UUID, fundraise_status_service: FundraiseStatusService = Depends(),
) -> ResponseBaseSchema:
    """GET '/fundraisers/{fundraise_id}/statuses' endpoint view function.

    Args:
        fundraise_id: UUID of a fundraise.
        fundraise_status_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with list of FundraiseStatusOutputSchema objects as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=[
            FundraiseStatusOutputSchema.from_orm(status) for status in
            await fundraise_status_service.get_fundraise_statuses(fundraise_id)
        ],
        errors=[],
    )


@fundraise_statuses_router.get('/{status_id}', response_model=ResponseBaseSchema)
async def get_fundraise_status(
        fundraise_id: UUID, status_id: UUID, fundraise_status_service: FundraiseStatusService = Depends(),
) -> ResponseBaseSchema:
    """GET '/fundraisers/{fundraise_id}/statuses/{status_id}' endpoint view function.

    Args:
        fundraise_id: UUID of a fundraise.
        status_id: UUID of a FundraiseStatus.
        fundraise_status_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with FundraiseStatusOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=FundraiseStatusOutputSchema.from_orm(
            await fundraise_status_service.get_fundraise_status_by_id(fundraise_id, status_id)
        ),
        errors=[],
    )


@fundraise_statuses_router.post('/', response_model=ResponseBaseSchema, status_code=status.HTTP_201_CREATED)
async def post_fundraise_statuses(
        fundraise_id: UUID, status_data: FundraiseStatusInputSchema,
        fundraise_status_service: FundraiseStatusService = Depends(), Authorize: AuthJWT = Depends(),
) -> ResponseBaseSchema:
    """POST '/fundraisers/{fundraise_id}/statuses' endpoint view function.

    Args:
        fundraise_id: UUID of a fundraise.
        status_data: Serialized FundraiseStatusInputSchema object.
        fundraise_status_service: dependency as business logic instance.
        Authorize: dependency of AuthJWT for JWT tokens.

    Returns:
    ResponseBaseSchema object with list of FundraiseStatusOutputSchema objects as response data.
    """
    Authorize.jwt_required()
    jwt_subject = Authorize.get_jwt_subject()

    return ResponseBaseSchema(
        status_code=status.HTTP_201_CREATED,
        data=FundraiseStatusOutputSchema.from_orm(
            await fundraise_status_service.add_fundraise_status(fundraise_id, jwt_subject, status_data)
        ),
        errors=[],
    )
