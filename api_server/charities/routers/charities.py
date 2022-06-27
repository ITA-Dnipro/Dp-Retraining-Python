from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status

from fastapi_jwt_auth import AuthJWT

from charities.routers.charity_employees import charity_employees_router
from charities.schemas import (  # AddManagerSchema,; CharityUpdateSchema,; ManagerResponseSchema,
    CharityFullOutputSchema,
    CharityInputSchema,
    CharityPaginatedOutputSchema,
    CharityUpdateSchema,
)
from charities.services.charities import CharityService
from common.constants.charities import CharityRouteConstants
from common.schemas.responses import ResponseBaseSchema

charities_router = APIRouter(prefix='/charities', tags=['Charities'])
charities_router.include_router(charity_employees_router, prefix='/{charity_id}')


@charities_router.post('/', response_model=ResponseBaseSchema, status_code=status.HTTP_201_CREATED)
async def post_charities(
        charity: CharityInputSchema,
        charity_service: CharityService = Depends(),
        Authorize: AuthJWT = Depends(),
):
    """POST '/charities' endpoint view function.

    Args:
        charity: Serialized CharityInputSchema object.
        charity_service: dependency as business logic instance.
        Authorize: dependency of AuthJWT for JWT tokens.

    Returns:
    ResponseBaseSchema object with CharityFullOutputSchema object as response data.
    """
    Authorize.jwt_required()
    jwt_subject = Authorize.get_jwt_subject()
    return ResponseBaseSchema(
        status_code=status.HTTP_201_CREATED,
        data=CharityFullOutputSchema.from_orm(await charity_service.add_charity(charity, jwt_subject)),
        errors=[],
    )


@charities_router.get('/', response_model=ResponseBaseSchema)
async def get_charities(
        page: int = Query(
            default=CharityRouteConstants.DEFAULT_START_PAGE.value,
            gt=CharityRouteConstants.ZERO_NUMBER.value,
        ),
        page_size: int = Query(
            default=CharityRouteConstants.DEFAULT_PAGE_SIZE.value,
            gt=CharityRouteConstants.ZERO_NUMBER.value,
            lt=CharityRouteConstants.MAX_PAGINATION_PAGE_SIZE.value,
        ),
        charity_service: CharityService = Depends(),
) -> ResponseBaseSchema:
    """GET '/charities' endpoint view function.

    Args:
        page: pagination page.
        page_size: pagination page size, how many items to show per page.
        charity_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with list of CharityOutputSchema objects as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=CharityPaginatedOutputSchema.from_orm(await charity_service.get_charities(page, page_size)),
        errors=[],
    )


@charities_router.get('/{id}', response_model=ResponseBaseSchema)
async def get_charity(
        id: UUID,
        charity_service: CharityService = Depends(),
) -> ResponseBaseSchema:
    """GET '/charities/{id}' endpoint view function.

    Args:
        id: UUID of charity.
        charity_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with CharityFullOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=CharityFullOutputSchema.from_orm(await charity_service.get_charity_by_id_with_relationships(id_=id)),
        errors=[],
    )


@charities_router.put('/{id}', response_model=ResponseBaseSchema)
async def put_charity(
        id: UUID,
        update_data: CharityUpdateSchema,
        charity_service: CharityService = Depends(),
        Authorize: AuthJWT = Depends(),
) -> ResponseBaseSchema:
    """PUT '/charities/{id}' endpoint view function.

    Args:
        id: UUID of charity.
        update_data: Serialized CharityUpdateSchema object.
        charity_service: dependency as business logic instance.
        Authorize: dependency of AuthJWT for JWT tokens.

    Returns:
    ResponseBaseSchema object with CharityFullOutputSchema object as response data.
    """
    Authorize.jwt_required()
    jwt_subject = Authorize.get_jwt_subject()

    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=CharityFullOutputSchema.from_orm(
            await charity_service.update_charity(id_=id, jwt_subject=jwt_subject, update_data=update_data)
        ),
        errors=[],
    )


@charities_router.delete('/{id}', response_model=ResponseBaseSchema)
async def delete_charity(
        id: UUID,
        charity_service: CharityService = Depends(),
        Authorize: AuthJWT = Depends(),
) -> ResponseBaseSchema:
    """DELETE '/charities/{id}' endpoint view function.

    Args:
        id: UUID of charity.
        charity_service: dependency as business logic instance.
        Authorize: dependency of AuthJWT for JWT tokens.

    Returns:
    http response with no data and 204 status code.
    """
    Authorize.jwt_required()
    jwt_subject = Authorize.get_jwt_subject()

    await charity_service.delete_charity(id_=id, jwt_subject=jwt_subject)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
