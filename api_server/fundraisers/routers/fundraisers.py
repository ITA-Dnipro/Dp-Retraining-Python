from fastapi import APIRouter, Depends, Query, status

from common.constants.fundraisers import FundraiseRouteConstants
from common.schemas.responses import ResponseBaseSchema
from fundraisers.schemas import FundraisePaginatedOutputSchema
from fundraisers.services import FundraiseService

fundraisers_router = APIRouter(prefix='/fundraisers', tags=['Fundraisers'])


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
