from uuid import UUID

from sqlalchemy import func, join
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import aliased, relationship, subqueryload

from charities.models import Charity, CharityEmployeeAssociation, CharityEmployeeRoleAssociation, Employee, EmployeeRole
from charities.schemas import CharityInputSchema
from utils.logging import setup_logging


class CharityDBService:

    def __init__(self, session: AsyncSession) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def get_charity_by_id(self, id_: UUID) -> Charity | None:
        """Get Charity object from database filtered by id.

        Args:
            id_: UUID of charity.

        Returns:
        Single Charity object filtered by id.
        """
        return await self._get_charity_by_id(id_)

    async def _get_charity_by_id(self, id_: UUID) -> Charity | None:
        return await self._select_charity(column='id', value=id_)

    async def _select_charity(self, column: str, value: UUID | str) -> Charity | None:
        self._log.debug(f'Getting Charity with "{column}": "{value}" from the db.')
        q = select(Charity).where(Charity.__table__.columns[column] == value)
        result = await self.session.execute(q)
        return result.scalars().one_or_none()

    async def add_charity(self, charity: CharityInputSchema) -> Charity:
        """Add Charity object to the database.

        Args:
            charity: CharityInputSchema object.

        Returns:
        Newly created Charity object.
        """
        return await self._add_charity(charity)

    async def _add_charity(self, charity: CharityInputSchema) -> Charity:
        db_charity = Charity(**charity.dict())
        self.session.add(db_charity)
        await self.session.commit()
        await self.session.refresh(db_charity)
        self._log.debug(f'Charity with id: "{db_charity.id}" successfully created.')
        return db_charity

    async def get_charity_by_id_with_relationships(self, id_: UUID) -> Charity | None:
        """Get Charity object from database filtered by id with loaded relationships.

        Args:
            id_: UUID of charity.

        Returns:
        Single Charity object filtered by id with loaded relationships.
        """
        return await self._get_charity_by_id_with_relationships(id_)

    async def _get_charity_by_id_with_relationships(self, id_: UUID) -> Charity | None:
        CharityEmployeeAssociation.roles = relationship(
            'EmployeeRole',
            secondary='charity_employee_role_association',
            lazy='subquery',
        )
        Charity.employees = relationship('Employee', secondary='charity_employee_association', lazy='subquery')
        roles_subquery = (
            select(EmployeeRole, CharityEmployeeAssociation).join(
                CharityEmployeeRoleAssociation, CharityEmployeeRoleAssociation.role_id == EmployeeRole.id
            ).subquery()
        )
        EmployeeRoleAlias = aliased(EmployeeRole, roles_subquery)
        Employee.roles = relationship(EmployeeRoleAlias, primaryjoin=Employee.id == roles_subquery.c.employee_id)
        q = select(Charity).where(Charity.id == id_).options(
            subqueryload(Charity.employees).subqueryload(Employee.roles),
        )
        result = await self.session.execute(q)
        return result.scalars().one_or_none()

    async def get_charities(self, page: int, page_size: int) -> list[Charity]:
        """Get Charity objects from database.

        Args:
            page: number of result page.
            page_size: number of items per page.

        Returns:
        list of Charity objects.
        """
        return await self._get_charities(page, page_size)

    async def _get_charities(self, page: int, page_size: int) -> list[Charity]:
        self._log.debug(f'Getting charities from the db, page: {page} with page size: {page_size}.')
        CharityEmployeeAssociation.roles = relationship(
            'EmployeeRole',
            secondary='charity_employee_role_association',
            lazy='subquery',
        )
        Charity.employees = relationship('Employee', secondary='charity_employee_association', lazy='subquery')
        roles_subquery = (
            select(EmployeeRole, CharityEmployeeAssociation).join(
                CharityEmployeeRoleAssociation, CharityEmployeeRoleAssociation.role_id == EmployeeRole.id
            ).subquery()
        )
        EmployeeRoleAlias = aliased(EmployeeRole, roles_subquery)
        Employee.roles = relationship(EmployeeRoleAlias, primaryjoin=Employee.id == roles_subquery.c.employee_id)
        q = select(Charity).limit(page_size).offset((page - 1) * page_size).options(
            subqueryload(Charity.employees).subqueryload(Employee.roles),
        )
        return (await self.session.execute(q)).scalars().all()

    async def get_total_charities(self) -> int:
        """Counts number of fundraisers in Fundraise table.

        Returns:
        Quantity of fundraise objects in Fundraise table.
        """
        return await self._get_total_charities()

    async def _get_total_charities(self) -> int:
        total_charities = (await self.session.execute(select(func.count(Charity.id)))).scalar_one()
        self._log.debug(f'Charity table has totally: "{total_charities}" charities.')
        return total_charities
