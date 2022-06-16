from uuid import UUID

from fastapi import Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from charities.db_services import CharityDBService, CharityEmployeeDBService
from charities.models import CharityOrganisation
from charities.utils.exceptions import OrganisationHTTPException
from db import get_session
from users.models import User
from utils.logging import setup_logging


class CharityCommonService:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.charity_db_service = CharityDBService(session)
        self.charity_employee_db_service = CharityEmployeeDBService(session)

    async def get_charity_by_id(self, id_: UUID) -> CharityOrganisation:
        """Get CharityOrganisation object from database filtered by id.

        Args:
            id_: UUID of charity.
        Raise:
            OrganisationHTTPException in case charity not found.

        Returns:
        single CharityOrganisation object filtered by id.
        """
        return await self._get_charity_by_id(id_)

    async def _get_charity_by_id(self, id_: UUID) -> CharityOrganisation:
        charity = await self.charity_db_service.get_charity_by_id(id_)
        if not charity:
            raise OrganisationHTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="This organisation hasn't been found",
            )
        return charity

    async def save_employee_to_charity(self, user: User, charity: CharityOrganisation) -> CharityOrganisation:
        """Save User to CharityOrganisation in the database via many-to-many relationship.

        Args:
            user: User object.
            charity: CharityOrganisation object.

        Returns:
        CharityOrganisation object with User added to many-to-many relationship.
        """
        return await self._save_employee_to_charity(user, charity)

    async def _save_employee_to_charity(self, user: User, charity: CharityOrganisation) -> CharityOrganisation:
        return await self.charity_employee_db_service.add_user_to_charity(user, charity)
