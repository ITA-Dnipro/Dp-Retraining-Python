from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from fundraisers.dao import FundraiseDAO
from fundraisers.models import Fundraise
from fundraisers.schemas import FundraiseInputSchema
from users.utils.pagination import PaginationPage
from utils.logging import setup_logging


class FundraiseService:

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.fundraise_dao = FundraiseDAO(session=self.session)

    async def get_fundraisers(self, page: int, page_size: int) -> PaginationPage:
        """Get Fundraise objects from database.

        Args:
            page: number of result page.
            page_size: number of items per page.

        Returns:
        PaginationPage object with items as a list of Fundraise objects.
        """
        return await self._get_fundraisers(page, page_size)

    async def _get_fundraisers(self, page: int, page_size: int) -> PaginationPage:
        fundraisers = await self.fundraise_dao.get_fundraisers(page, page_size)
        total_fundraisers = await self.fundraise_dao._get_total_fundraisers()
        return PaginationPage(items=fundraisers, page=page, page_size=page_size, total=total_fundraisers)

    async def add_fundraise(self, fundraise: FundraiseInputSchema) -> Fundraise:
        """Add Fundraise object to the database.

        Args:
            fundraise: FundraiseInputSchema object.

        Returns:
        Newly created Fundraise object.
        """
        return await self._add_fundraise(fundraise)

    async def _add_fundraise(self, fundraise: FundraiseInputSchema) -> Fundraise:
        return await self.fundraise_dao.add_fundraise(fundraise)
