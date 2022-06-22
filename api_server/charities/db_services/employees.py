from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from charities.models import Employee
from charities.schemas import EmployeeDBSchema
from utils.logging import setup_logging


class EmployeeDBService:
    """Container class with methods for common CRUD operations for Employee model.

    Raise:
        sqlalchemy exceptions like IntegrityError etc.

    Returns:
    Employee object or None.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def get_employee_by_user_id(self, user_id: UUID) -> Employee | None:
        """Get Employee object from database filtered by user_id.

        Args:
            user_id: of employee.

        Returns:
        single Employee object filtered by user_id.
        """
        return await self._get_employee_by_user_id(user_id)

    async def _get_employee_by_user_id(self, user_id: UUID) -> Employee | None:
        return await self._select_employee(column='user_id', value=user_id)

    async def _select_employee(self, column: str, value: UUID | str) -> Employee | None:
        self._log.debug(f'Getting Employee with "{column}": "{value}" from the db.')
        q = select(Employee).where(Employee.__table__.columns[column] == value)
        result = await self.session.execute(q)
        return result.scalars().one_or_none()

    async def add_employee(self, employee: EmployeeDBSchema) -> Employee:
        """Add Employee object to the database.

        Args:
            fundraise: EmployeeDBSchema object.

        Returns:
        Newly created Employee object.
        """
        return await self._add_employee(employee)

    async def _add_employee(self, employee: EmployeeDBSchema) -> Employee:
        db_employee = Employee(**employee.dict())
        self.session.add(db_employee)
        await self.session.commit()
        await self.session.refresh(db_employee)
        self._log.debug(f'Employee with id: "{db_employee.id}" successfully created.')
        return db_employee
