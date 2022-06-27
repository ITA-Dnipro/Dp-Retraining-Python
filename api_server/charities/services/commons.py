from uuid import UUID

from fastapi import Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from charities.db_services import CharityDBService, CharityEmployeeDBService
from charities.models import Charity, Employee
from charities.utils.exceptions import CharityNotFoundError
from common.exceptions.charities import CharityExceptionMsgs
from db import get_session
from utils.logging import setup_logging


class CharityCommonService:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.charity_db_service = CharityDBService(session)
        self.charity_employee_db_service = CharityEmployeeDBService(session)

    async def get_charity_by_id(self, id_: UUID) -> Charity:
        """Get Charity object from database filtered by id.

        Args:
            id_: UUID of charity.
        Raise:
            OrganisationHTTPException in case charity not found.

        Returns:
        single Charity object filtered by id.
        """
        return await self._get_charity_by_id(id_)

    async def _get_charity_by_id(self, id_: UUID) -> Charity:
        charity = await self.charity_db_service.get_charity_by_id(id_)
        if not charity:
            err_msg = CharityExceptionMsgs.CHARITY_NOT_FOUND.value.format(
                column='id',
                value=id_,
            )
            self._log.debug(err_msg)
            raise CharityNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return charity

    async def save_employee_to_charity(self, employee: Employee, charity: Charity) -> Charity:
        """Save Employee to Charity in the database via many-to-many relationship.

        Args:
            employee: Employee object.
            charity: Charity object.

        Returns:
        Charity object with Employee added to many-to-many relationship.
        """
        return await self._save_employee_to_charity(employee, charity)

    async def _save_employee_to_charity(self, employee: Employee, charity: Charity) -> Charity:
        return await self.charity_employee_db_service.add_employee_to_charity(employee, charity)

    async def get_charity_by_id_with_relationships(self, id_: UUID) -> Charity:
        """Get Charity object from database filtered by id with loaded relationships.

        Args:
            id_: UUID of charity.
        Raise:
            CharityNotFoundError in case fundraise not found.

        Returns:
        single Fundraise object filtered by id.
        """
        return await self._get_get_charity_by_id_with_relationships(id_)

    async def _get_get_charity_by_id_with_relationships(self, id_: UUID) -> Charity:
        charity = await self.charity_db_service.get_charity_by_id_with_relationships(id_)
        if not charity:
            err_msg = CharityExceptionMsgs.CHARITY_NOT_FOUND.value.format(
                column='id',
                value=id_,
            )
            self._log.debug(err_msg)
            raise CharityNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return await self.charity_db_service.refresh_charity(charity)

    async def count_employee_role_in_charity(self, charity: Charity, role_name: str) -> int:
        """Counts how many Charity.employees have specific role.

        Args:
            charity: Charity object.
            role_name: Employee role name.

        Returns:
        int of how many Charity.employees have specific role.
        """
        return await self._count_employee_role_in_charity(charity, role_name)

    async def _count_employee_role_in_charity(self, charity: Charity, role_name: str) -> int:
        total_roles = 0
        for employee in charity.employees:
            for role in employee.roles:
                if role.name == role_name:
                    total_roles += 1
        return total_roles

    async def employee_has_role(self, employee: Employee, role_name: str) -> bool:
        """Check if Employee have a role with provided role name.

        Args:
            employee: Employee object.
            role_name: Employee role name.

        Returns:
        bool of check if Employee have a role with provided role name.
        """
        return await self._employee_has_role(employee, role_name)

    async def _employee_has_role(self, employee: Employee, role_name: str) -> bool:
        return any(role_name == employee_role.name for employee_role in employee.roles)
