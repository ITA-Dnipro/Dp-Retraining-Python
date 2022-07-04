from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status

from fastapi_jwt_auth import AuthJWT

from common.constants.fundraisers import FundraiseRouteConstants
from common.schemas.responses import ResponseBaseSchema
from fundraisers.routers.fundraise_statuses import fundraise_statuses_router
from fundraisers.schemas import (
    FundraiseFullOutputSchema,
    FundraiseInputSchema,
    FundraisePaginatedOutputSchema,
    FundraiseUpdateSchema,
)
from fundraisers.services import FundraiseService

fundraisers_router = APIRouter(prefix='/fundraisers', tags=['Fundraisers'])
fundraisers_router.include_router(fundraise_statuses_router, prefix='/{fundraise_id}')


@fundraisers_router.get('/', response_model=ResponseBaseSchema)
async def get_fundraisers(
        page: int = Query(
            default=FundraiseRouteConstants.DEFAULT_START_PAGE.value,
            gt=FundraiseRouteConstants.ZERO_NUMBER.value,
        ),
        page_size: int = Query(
            default=FundraiseRouteConstants.DEFAULT_PAGE_SIZE.value,
            gt=FundraiseRouteConstants.ZERO_NUMBER.value,
            lt=FundraiseRouteConstants.MAX_PAGINATION_PAGE_SIZE.value,
        ),
        fundraise_service: FundraiseService = Depends()
) -> ResponseBaseSchema:
    """GET '/fundraisers' endpoint view function.

    Args:
        page: pagination page.
        page_size: pagination page size, how many items to show per page.
        fundraise_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with list of FundraiseFullOutputSchema objects as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=FundraisePaginatedOutputSchema.from_orm(await fundraise_service.get_fundraisers(page, page_size)),
        errors=[],
    )


@fundraisers_router.post('/', response_model=ResponseBaseSchema, status_code=status.HTTP_201_CREATED)
async def post_fundraisers(
        fundraise: FundraiseInputSchema,
        fundraise_service: FundraiseService = Depends(),
        Authorize: AuthJWT = Depends(),
) -> ResponseBaseSchema:
    """POST '/fundraisers' endpoint view function.

    Args:
        fundraise: Serialized FundraiseInputSchema object.
        fundraise_service: dependency as business logic instance.
        Authorize: dependency of AuthJWT for JWT tokens.

    Returns:
    ResponseBaseSchema object with FundraiseFullOutputSchema object as response data.
    """
    Authorize.jwt_required()
    jwt_subject = Authorize.get_jwt_subject()
    return ResponseBaseSchema(
        status_code=status.HTTP_201_CREATED,
        data=FundraiseFullOutputSchema.from_orm(await fundraise_service.add_fundraise(fundraise, jwt_subject)),
        errors=[],
    )


@fundraisers_router.get('/{id}', response_model=ResponseBaseSchema)
async def get_fundraise(
        id: UUID,
        fundraise_service: FundraiseService = Depends()
) -> ResponseBaseSchema:
    """GET '/fundraisers/{id}' endpoint view function.

    Args:
        id: UUID of fundraise.
        fundraise_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with FundraiseFullOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=FundraiseFullOutputSchema.from_orm(await fundraise_service.get_fundraise_by_id(id_=id)),
        errors=[],
    )


@fundraisers_router.put('/{id}', response_model=ResponseBaseSchema)
async def put_fundraise(
        id: UUID,
        update_data: FundraiseUpdateSchema,
        fundraise_service: FundraiseService = Depends(),
        Authorize: AuthJWT = Depends(),
) -> ResponseBaseSchema:
    """PUT '/fundraisers/{id}' endpoint view function.

    Args:
        id: UUID of fundraise.
        update_data: Serialized FundraiseUpdateSchema object.
        fundraise_service: dependency as business logic instance.
        Authorize: dependency of AuthJWT for JWT tokens.

    Returns:
    ResponseBaseSchema object with FundraiseFullOutputSchema object as response data.
    """
    Authorize.jwt_required()
    jwt_subject = Authorize.get_jwt_subject()
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=FundraiseFullOutputSchema.from_orm(
            await fundraise_service.update_fundraise(id_=id, jwt_subject=jwt_subject, update_data=update_data)
        ),
        errors=[],
    )


@fundraisers_router.delete('/{id}')
async def delete_fundraise(
        id: UUID,
        fundraise_service: FundraiseService = Depends(),
        Authorize: AuthJWT = Depends(),
) -> Response:
    """DELETE '/fundraisers/{id}' endpoint view function.

    Args:
        id: UUID of fundraise.
        fundraise_service: dependency as business logic instance.
        Authorize: dependency of AuthJWT for JWT tokens.

    Returns:
    http response with no data and 204 status code.
    """
    Authorize.jwt_required()
    jwt_subject = Authorize.get_jwt_subject()
    await fundraise_service.delete_fundraise(id_=id, jwt_subject=jwt_subject)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
