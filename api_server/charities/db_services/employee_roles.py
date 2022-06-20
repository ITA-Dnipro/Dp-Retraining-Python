from uuid import UUID

from sqlalchemy import join
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased, relationship, subqueryload

from charities.models import Charity, CharityEmployeeAssociation, CharityEmployeeRoleAssociation, Employee, EmployeeRole
from charities.schemas import EmployeeRoleInputSchema
from utils.logging import setup_logging


class EmployeeRoleDBService:
    """Container class with methods for common CRUD operations for EmployeeRole model.

    Raise:
        sqlalchemy exceptions like IntegrityError etc.

    Returns:
    EmployeeRole object or None.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def get_employee_role_by_name(self, name: str) -> EmployeeRole | None:
        """Get EmployeeRole object from database filtered by name.

        Args:
            name: of employee role.

        Returns:
        single EmployeeRole object filtered by name.
        """
        return await self._get_employee_role_by_name(name)

    async def _get_employee_role_by_name(self, name: str) -> EmployeeRole | None:
        return await self._select_employee_role(column='name', value=name)

    async def _select_employee_role(self, column: str, value: UUID | str) -> EmployeeRole | None:
        self._log.debug(f'Getting EmployeeRole with "{column}": "{value}" from the db.')
        q = select(EmployeeRole).where(EmployeeRole.__table__.columns[column] == value)
        result = await self.session.execute(q)
        return result.scalars().one_or_none()

    async def add_employee_role(self, employee_role: EmployeeRoleInputSchema) -> EmployeeRole:
        """Add EmployeeRole object to the database.

        Args:
            fundraise: EmployeeRoleInputSchema object.

        Returns:
        Newly created EmployeeRole object.
        """
        return await self._add_employee_role(employee_role)

    async def _add_employee_role(self, employee_role: EmployeeRoleInputSchema) -> EmployeeRole:
        db_employee_role = EmployeeRole(**employee_role.dict())
        self.session.add(db_employee_role)
        await self.session.commit()
        await self.session.refresh(db_employee_role)
        self._log.debug(f'EmployeeRole with name: "{db_employee_role.name}" successfully created.')
        return db_employee_role

    async def add_role_to_charity_employee(
            self, role: EmployeeRole, charity_employee: CharityEmployeeAssociation,
    ) -> CharityEmployeeRoleAssociation:
        """Add EmployeeRole to CharityEmployeeAssociation in the database via many-to-many relationship.

        Args:
            employee: Employee object.
            charity: Charity object.

        Returns:
        CharityEmployeeAssociation object with EmployeeRole added to many-to-many relationship.
        """
        return await self._add_role_to_charity_employee(role, charity_employee)

    async def _add_role_to_charity_employee(
            self, role: EmployeeRole, charity_employee: CharityEmployeeAssociation,
    ) -> CharityEmployeeRoleAssociation:
        charity_employee_role_association = CharityEmployeeRoleAssociation()
        charity_employee_role_association.role_id = role.id
        charity_employee_role_association.charity_employee_id = charity_employee.id
        self.session.add(charity_employee_role_association)
        await self.session.commit()
        await self.session.refresh(charity_employee_role_association)
        self._log.debug(
            f'EmployeeRole with name: "{role.name}" added to CharityEmployeeAssociation with id: {charity_employee.id}.'
        )
        return charity_employee_role_association
