from uuid import UUID

from fastapi import status

from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from charities.models import Charity, CharityEmployeeAssociation, Employee
from charities.utils.exceptions import CharityEmployeeDuplicateError
from common.exceptions.charities import CharityEmployeesExceptionMsgs
from utils.logging import setup_logging


class CharityEmployeeDBService:

    def __init__(self, session: AsyncSession) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def add_employee_to_charity(self, employee: Employee, charity: Charity) -> CharityEmployeeAssociation:
        """Add Employee to Charity in the database via many-to-many relationship.

        Args:
            employee: Employee object.
            charity: Charity object.

        Returns:
        Charity object with Employee added to many-to-many relationship.
        """
        return await self._add_employee_to_charity(employee, charity)

    async def _add_employee_to_charity(self, employee: Employee, charity: Charity) -> CharityEmployeeAssociation:
        charity_employee_association = CharityEmployeeAssociation()
        charity_employee_association.charity_id = charity.id
        charity_employee_association.employee_id = employee.id
        self.session.add(charity_employee_association)
        try:
            await self.session.commit()
        except IntegrityError as exc:
            err_msg = CharityEmployeesExceptionMsgs.EMPLOYEE_ALREADY_IN_CHARITY.value.format(
                employee_id=charity_employee_association.employee_id,
                charity_id=charity_employee_association.charity_id,
            )
            self._log.debug(exc)
            await self.session.rollback()
            raise CharityEmployeeDuplicateError(status_code=status.HTTP_400_BAD_REQUEST, detail=err_msg)
        await self.session.refresh(charity_employee_association)
        self._log.debug(
            f'Employee with id: "{employee.id}" added to Charity with id: {charity.id}.'
        )
        return charity_employee_association

    async def remove_employee_from_charity(self, charity: Charity, employee: Employee) -> None:
        """Removes Employee from Charity.employees collection.

        Args:
            charity: Charity object.
            employee: Employee object.

        Returns:
        Nothing.
        """
        return await self._remove_employee_from_charity(charity, employee)

    async def _remove_employee_from_charity(self, charity: Charity, employee: Employee) -> None:
        charity.employees.remove(employee)
        await self.session.commit()
        self._log.debug(f'Employee with id: "{employee.id}" removed from Charity with id: {charity.id}.')

    async def get_charity_employee_by_charity_and_employee_id(
            self, charity_id: UUID, employee_id: UUID,
    ) -> CharityEmployeeAssociation | None:
        """Get CharityEmployeeAssociation object from database filtered by charity_id and employee_id.

        Args:
            charity_id: UUID of a Charity object.
            employee_id: UUID of a Employee object.

        Returns:
        Single CharityEmployeeAssociation filtered by charity_id and employee_id.
        """
        return await self._get_charity_employee_by_charity_and_employee_id(charity_id, employee_id)

    async def _get_charity_employee_by_charity_and_employee_id(
            self, charity_id: UUID, employee_id: UUID,
    ) -> CharityEmployeeAssociation | None:
        q = select(CharityEmployeeAssociation).where(
            and_(
                CharityEmployeeAssociation.charity_id == charity_id,
                CharityEmployeeAssociation.employee_id == employee_id,
            )
        )
        result = await self.session.execute(q)
        return result.scalars().one_or_none()
