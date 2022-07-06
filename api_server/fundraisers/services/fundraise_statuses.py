from uuid import UUID

from fastapi import Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from common.constants.fundraisers import FundraiseStatusConstants
from common.exceptions.fundraisers import FundraiseStatusExceptionMsgs
from db import get_session
from fundraisers.db_services import FundraiseStatusDBService
from fundraisers.models import Fundraise, FundraiseStatus
from fundraisers.schemas import FundraiseIsDonatableUpdateSchema, FundraiseStatusInputSchema
from fundraisers.services.fundraisers import FundraiseService
from fundraisers.utils.exceptions import FundraiseStatusNotFoundError, FundraiseStatusPermissionError
from fundraisers.utils.fundraise_statuses_helpers import (
    fundraise_status_validator,
    get_allowed_statuses_for_fundraise_status,
)
from fundraisers.utils.jwt import jwt_fundraise_validator
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

    async def add_fundraise_status(
            self, fundraise_id: UUID, jwt_subject: str, status_data: FundraiseStatusInputSchema,
    ) -> FundraiseStatus:
        """Add FundraiseStatus object to 'Fundraise.statuses' collection.

        Args:
            fundraise_id: UUID of a Fundraise object.
            jwt_subject: decoded jwt identity.
            status_data: Serialized FundraiseStatusInputSchema object.

        Returns:
        Added to 'Fundraise.statuses' collection FundraiseStatus object.
        """
        return await self._add_fundraise_status(fundraise_id, jwt_subject, status_data)

    async def _add_fundraise_status(
            self, fundraise_id: UUID, jwt_subject: str, status_data: FundraiseStatusInputSchema,
    ) -> FundraiseStatus:
        # Checking if currently authenticated employee listed in this charity.
        db_fundraise = await self.fundraise_service.get_fundraise_by_id(fundraise_id)
        usernames = [employee.user.username for employee in db_fundraise.charity.employees]
        if jwt_fundraise_validator(jwt_subject=jwt_subject, usernames=usernames):
            allowed_statuses = get_allowed_statuses_for_fundraise_status(
                status_name=status_data.name,
                allowed_statuses=FundraiseStatusConstants.ADD_STATUS_MAPPING.value
            )
            new_status = await self.get_fundraise_status_by_name(name=status_data.name)
            # Checking if status can be added.
            db_fundraise_last_status = db_fundraise.statuses[-1]
            if not fundraise_status_validator(
                    fundraise_status_name=db_fundraise_last_status.status.name,
                    allowed_statuses=allowed_statuses):
                raise FundraiseStatusPermissionError(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=FundraiseStatusExceptionMsgs.FUNDRAISE_STATUS_NOT_PERMITTED.value.format(
                        field_name='name',
                        field_value=new_status.name,
                    ),
                )
            added_fundraise_status = await self.fundraise_status_db_service.add_status_to_fundraise(
                fundraise=db_fundraise,
                fundraise_status=new_status,
            )
            # Setting Fundraise.is_donatable field based on newly added status.
            added_fundraise_status_is_donatable_status = (
                FundraiseStatusConstants.FUNDRAISE_IS_DONATABLE_STATUS_MAPPING.value[added_fundraise_status.name]
            )
            if db_fundraise.is_donatable != added_fundraise_status_is_donatable_status:
                self._log.debug(
                    f'Changing Fundraise.is_donatable status from: "{db_fundraise.is_donatable}" '
                    f'to: "{added_fundraise_status_is_donatable_status}".'
                )
                new_is_donatable_status = FundraiseIsDonatableUpdateSchema(
                    is_donatable=added_fundraise_status_is_donatable_status,
                )
                await self.fundraise_service.update_fundraise_is_donatable_status(
                    id_=db_fundraise.id,
                    update_data=new_is_donatable_status,
                )
            return added_fundraise_status

    async def get_fundraise_status_by_name(self, name: str) -> FundraiseStatus:
        """Get FundraiseStatus object from database filtered by name.

        Args:
            name: of FundraiseStatus object.

        Raise:
            FundraiseStatusNotFoundError in case status not found in FundraiseStatus table.

        Returns:
        Single FundraiseStatus object filtered by name.
        """
        return await self._get_fundraise_status_by_name(name)

    async def _get_fundraise_status_by_name(self, name: str) -> FundraiseStatus:
        db_fundraise_status = await self.fundraise_status_db_service.get_fundraise_status_by_name(name)
        if not db_fundraise_status:
            err_msg = FundraiseStatusExceptionMsgs.FUNDRAISE_STATUS_NOT_SUPPORTED.value.format(
                field_name='name',
                field_value=name,
            )
            self._log.debug(err_msg)
            raise FundraiseStatusNotFoundError(status_code=status.HTTP_400_BAD_REQUEST, detail=err_msg)
        return db_fundraise_status
