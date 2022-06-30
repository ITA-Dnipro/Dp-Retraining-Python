from uuid import UUID

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from fundraisers.db_services import FundraiseStatusDBService
from fundraisers.models import FundraiseStatus
from fundraisers.services.fundraisers import FundraiseService
from utils.logging import setup_logging


class FundraiseStatusService:

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.fundraise_status_db_service = FundraiseStatusDBService(session=self.session)
        self.fundraise_service = FundraiseService(session=self.session)

    async def get_fundraise_statuses(self, fundraise_id: UUID) -> list[FundraiseStatus]:
        """Get fundraise's FundraiseStatus objects from database.

        Args:
            fundraise_id: UUID of a Fundraise object.

        Returns:
        list of fundraise's FundraiseStatus objects.
        """
        return await self._get_fundraise_statuses(fundraise_id)

    async def _get_fundraise_statuses(self, fundraise_id: UUID) -> list[FundraiseStatus]:
        db_fundraise = await self.fundraise_service.get_fundraise_by_id(fundraise_id)
        return db_fundraise.statuses
