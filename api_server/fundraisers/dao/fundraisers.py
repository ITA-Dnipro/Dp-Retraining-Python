from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fundraisers.models import Fundraise
from fundraisers.schemas import FundraiseInputSchema
from utils.logging import setup_logging


class FundraiseDAO:

    def __init__(self, session: AsyncSession) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def get_fundraisers(self, page: int, page_size: int) -> list[Fundraise]:
        """Get Fundraise objects from database.

        Args:
            page: number of result page.
            page_size: number of items per page.

        Returns:
        list of Fundraise objects.
        """
        return await self._get_fundraisers(page, page_size)

    async def _get_fundraisers(self, page: int, page_size: int) -> None:
        self._log.debug(f'Getting fundraisers from the db, page: {page} with page size: {page_size}.')
        q = select(Fundraise).limit(page_size).offset((page - 1) * page_size)
        return (await self.session.execute(q)).scalars().all()

    async def _get_total_fundraisers(self) -> int:
        """Counts number of fundraisers in Fundraise table.

        Returns:
        Quantity of fundraise objects in Fundraise table.
        """
        total_fundraisers = (await self.session.execute(select(func.count(Fundraise.id)))).scalar_one()
        self._log.debug(f'Fundraise table has totally: "{total_fundraisers}" fundraisers.')
        return total_fundraisers

    async def add_fundraise(self, fundraise: FundraiseInputSchema) -> Fundraise:
        """Add Fundraise object to the database.

        Args:
            fundraise: FundraiseInputSchema object.

        Returns:
        Newly created Fundraise object.
        """
        return await self._add_fundraise(fundraise)

    async def _add_fundraise(self, fundraise: FundraiseInputSchema) -> Fundraise:
        db_fundraise = Fundraise(**fundraise.dict())
        self.session.add(db_fundraise)
        await self.session.commit()
        await self.session.refresh(db_fundraise)
        self._log.debug(f'Fundraise with id: "{db_fundraise.id}" successfully created.')
        return db_fundraise
