from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from charities.models import CharityOrganisation
from charities.schemas import CharityInputSchema
from utils.logging import setup_logging


class CharityDBService:

    def __init__(self, session: AsyncSession) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def get_charity_by_id(self, id_: UUID) -> CharityOrganisation | None:
        """Get CharityOrganisation object from database filtered by id.

        Args:
            id_: UUID of charity.

        Returns:
        Single CharityOrganisation object filtered by id.
        """
        return await self._get_charity_by_id(id_)

    async def _get_charity_by_id(self, id_: UUID) -> CharityOrganisation | None:
        return await self._select_charity(column='id', value=id_)

    async def _select_charity(self, column: str, value: UUID | str) -> CharityOrganisation | None:
        self._log.debug(f'Getting CharityOrganisation with "{column}": "{value}" from the db.')
        q = select(CharityOrganisation).where(CharityOrganisation.__table__.columns[column] == value)
        result = await self.session.execute(q)
        return result.scalars().one_or_none()

    async def add_charity(self, charity: CharityInputSchema) -> CharityOrganisation:
        """Add CharityOrganisation object to the database.

        Args:
            charity: CharityInputSchema object.

        Returns:
        Newly created CharityOrganisation object.
        """
        return await self._add_charity(charity)

    async def _add_charity(self, charity: CharityInputSchema) -> CharityOrganisation:
        db_charity = CharityOrganisation(**charity.dict())
        self.session.add(db_charity)
        await self.session.commit()
        await self.session.refresh(db_charity)
        self._log.debug(f'CharityOrganisation with id: "{db_charity.id}" successfully created.')
        return db_charity
