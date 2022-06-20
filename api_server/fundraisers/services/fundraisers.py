from uuid import UUID

from fastapi import Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from common.constants.prepopulates.fundraise_statuses import FundraiseStatusPopulateData
from common.exceptions.fundraisers import FundraiseExceptionMsgs
from db import get_session
from fundraisers.dao import FundraiseDAO, FundraiseStatusDAO
from fundraisers.models import Fundraise
from fundraisers.schemas import FundraiseInputSchema, FundraiseUpdateSchema
from fundraisers.utils.exceptions import FundraiseNotFoundError
from fundraisers.utils.jwt import jwt_fundraise_validator
from utils.logging import setup_logging
from utils.pagination import PaginationPage


class FundraiseService:

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.fundraise_dao = FundraiseDAO(session=self.session)
        self.fundraise_status_dao = FundraiseStatusDAO(session=self.session)

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
        db_fundraise = await self.fundraise_dao.add_fundraise(fundraise)
        db_fundraise_status = await self.fundraise_status_dao.get_fundraise_status_by_name(
            FundraiseStatusPopulateData.NEW.value,
        )
        await self.fundraise_dao.add_status(fundraise=db_fundraise, fundraise_status=db_fundraise_status)
        return db_fundraise

    async def get_fundraise_by_id(self, id_: UUID) -> Fundraise:
        """Get Fundraise object from database filtered by id.

        Args:
            id_: UUID of fundraise.
        Raise:
            FundraiseNotFoundError in case fundraise not found.

        Returns:
        single Fundraise object filtered by id.
        """
        return await self._get_fundraise_by_id(id_)

    async def _get_fundraise_by_id(self, id_: UUID) -> Fundraise:
        fundraise = await self.fundraise_dao.get_fundraise_by_id(id_)
        if not fundraise:
            err_msg = FundraiseExceptionMsgs.FUNDRAISE_NOT_FOUND.value.format(
                column='id',
                value=id_,
            )
            self._log.debug(err_msg)
            raise FundraiseNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return fundraise

    async def update_fundraise(self, id_: UUID, jwt_subject: str, update_data: FundraiseUpdateSchema) -> Fundraise:
        """Updates Fundraise object data in the db.

        Args:
            id_: UUID of a Fundaise object.
            jwt_subject: decoded jwt identity.
            update_data: Serialized FundraiseUpdateSchema object.
        Raise:
            FundraisePermissionError in case of user not present in charity users list.
        Returns:
        Updated Fundraise object.
        """
        return await self._update_fundraise(id_, jwt_subject, update_data)

    async def _update_fundraise(self, id_: UUID, jwt_subject: str, update_data: FundraiseUpdateSchema) -> Fundraise:
        fundraise = await self.get_fundraise_by_id(id_)
        usernames = [user.username for user in fundraise.charity.users]
        if jwt_fundraise_validator(jwt_subject=jwt_subject, usernames=usernames):
            return await self.fundraise_dao.update_fundraise(id_, update_data)

    async def delete_fundraise(self, id_: UUID, jwt_subject: str) -> None:
        """Delete Fundraise object from the database.

        Args:
            id_: UUID of a Fundaise object.
            jwt_subject: decoded jwt identity.

        Returns:
        Nothing.
        """
        return await self._delete_fundraise(id_, jwt_subject)

    async def _delete_fundraise(self, id_: UUID, jwt_subject: str) -> None:
        fundraise = await self.get_fundraise_by_id(id_)
        usernames = [user.username for user in fundraise.charity.users]
        if jwt_fundraise_validator(jwt_subject=jwt_subject, usernames=usernames):
            return await self.fundraise_dao.delete_fundraise(fundraise)
