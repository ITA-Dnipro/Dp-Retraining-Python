from uuid import UUID

from fastapi import Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from common.exceptions.fundraisers import FundraiseStatusExceptionMsgs
from db import get_session
from fundraisers.db_services import FundraiseStatusDBService
from fundraisers.models import Fundraise, FundraiseStatus
from fundraisers.services.fundraisers import FundraiseService
from fundraisers.utils.exceptions import FundraiseStatusNotFoundError
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

    async def get_fundraise_status_by_id(self, fundraise_id: UUID, status_id: UUID) -> FundraiseStatus:
        """Get fundraise's FundraiseStatus object from database filtered by id.

        Args:
            fundraise_id: UUID of a Fundraise object.
            status_id: UUID of a FundraiseStatus.

        Returns:
        fundraise's FundraiseStatus object filtered by id.
        """
        return await self._get_fundraise_status_by_id(fundraise_id, status_id)

    async def _get_fundraise_status_by_id(self, fundraise_id: UUID, status_id: UUID) -> FundraiseStatus:
        db_fundraise = await self.fundraise_service.get_fundraise_by_id(fundraise_id)
        return await self.get_status_from_fundraise_by_id(fundraise=db_fundraise, status_id=status_id)

    async def get_status_from_fundraise_by_id(self, fundraise: Fundraise, status_id: UUID):
        """Get FundraiseStatus object by id from 'Fundraise.statuses' collection.

        Args:
            fundraise: Fundraise object.
            status_id: UUID of a FundraiseStatus.

        Raise:
            FundraiseStatusNotFoundError in case status not present in 'Fundraise.statuses' collection.

        Returns:
        Single fundraise's FundraiseStatus object filtered by id.
        """
        return await self._get_status_from_fundraise_by_id(fundraise, status_id)

    async def _get_status_from_fundraise_by_id(self, fundraise: Fundraise, status_id: UUID):
        for fundraise_status in fundraise.statuses:
            if fundraise_status.id == status_id:
                break
        else:
            err_msg = FundraiseStatusExceptionMsgs.FUNDRAISE_STATUS_NOT_FOUND_IN_FUNDRAISE.value.format(
                    field_name='id',
                    field_value=status_id,
                    fundraise_id=fundraise.id,
                )
            self._log.debug(err_msg)
            raise FundraiseStatusNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return fundraise_status
