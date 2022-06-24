from uuid import UUID

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from charities.models import EmployeeRole
from charities.services.charity_employees import CharityEmployeeService
from charities.services.commons import CharityCommonService
from db import get_session
from utils.logging import setup_logging


class EmployeeRoleService(CharityCommonService):

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session)
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.charity_employee_service = CharityEmployeeService(session)

    async def get_employee_roles(self, charity_id: UUID, employee_id: UUID) -> list[EmployeeRole]:
        """Get employee's EmployeeRole objects from the database.

        Args:
            charity_id: UUID of charity.
            employee_id: UUID of employee.

        Returns:
        list of employee's EmployeeRole objects.
        """
        return await self._get_employee_roles(charity_id, employee_id)

    async def _get_employee_roles(self, charity_id: UUID, employee_id: UUID) -> list[EmployeeRole]:
        db_charity = await self.get_charity_by_id_with_relationships(charity_id)
        db_charity_employee = await self.charity_employee_service.get_employee_from_charity(db_charity, employee_id)
        return db_charity_employee.roles
