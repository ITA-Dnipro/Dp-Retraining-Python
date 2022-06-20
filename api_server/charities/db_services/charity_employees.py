from sqlalchemy.ext.asyncio import AsyncSession

from charities.models import Charity, CharityEmployeeAssociation, Employee
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
        await self.session.commit()
        await self.session.refresh(charity_employee_association)
        self._log.debug(
            f'Employee with id: "{employee.id}" added to Charity with id: {charity.id}.'
        )
        return charity_employee_association
