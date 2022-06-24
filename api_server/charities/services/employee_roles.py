from uuid import UUID

from fastapi import Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from charities.models import Employee, EmployeeRole
from charities.services.charity_employees import CharityEmployeeService
from charities.services.commons import CharityCommonService
from charities.utils.exceptions import EmployeeRoleNotFoundError
from common.exceptions.charities import EmployeeRolesExceptionMsgs
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

    async def get_employee_role_by_id(self, charity_id: UUID, employee_id: UUID, role_id: UUID) -> EmployeeRole:
        """Get employee's EmployeeRole object from the database filtered by id.

        Args:
            charity_id: UUID of charity.
            employee_id: UUID of employee.
            role_id: UUID of EmployeeRole.

        Returns:
        Single employee's EmployeeRole object filtered by id.
        """
        return await self._get_employee_role_by_id(charity_id, employee_id, role_id)

    async def _get_employee_role_by_id(self, charity_id: UUID, employee_id: UUID, role_id: UUID) -> EmployeeRole:
        db_charity = await self.get_charity_by_id_with_relationships(charity_id)
        db_charity_employee = await self.charity_employee_service.get_employee_from_charity(db_charity, employee_id)
        return await self.get_role_from_employee_by_id(db_charity_employee, role_id)

    async def get_role_from_employee_by_id(self, employee: Employee, role_id: UUID) -> EmployeeRole:
        """Get EmployeeRole object from Employee.roles collection filtered by id.

        Args:
            employee: Employee object.
            role_id: UUID of a EmployeeRole object.

        Raise:
            EmployeeRoleNotFoundError in case EmployeeRole not present in Employee.roles collection.

        Returns:
        Single employee's EmployeeRole object filtered by id.
        """
        return await self._get_role_from_employee_by_id(employee, role_id)

    async def _get_role_from_employee_by_id(self, employee: Employee, role_id: UUID) -> EmployeeRole:
        for role in employee.roles:
            if role.id == role_id:
                break
        else:
            err_msg = EmployeeRolesExceptionMsgs.ROLE_NOT_FOUND.value.format(
                role_id=role_id,
                employee_id=employee.id,
            )
            self._log.debug(err_msg)
            raise EmployeeRoleNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return role
