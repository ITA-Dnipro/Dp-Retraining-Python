from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fundraisers.models import FundraiseStatus
from fundraisers.schemas import FundraiseStatusInputSchema
from utils.logging import setup_logging


class FundraiseStatusDBService:

    def __init__(self, session: AsyncSession) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def get_fundraise_status_by_name(self, name: str) -> FundraiseStatus:
        """Get FundraiseStatus object from database filtered by name.

        Args:
            name: of fundraise status.

        Returns:
        single FundraiseStatus object filtered by name.
        """
        return await self._get_fundraise_status_by_name(name)

    async def _get_fundraise_status_by_name(self, name: str) -> FundraiseStatus | None:
        return await self._select_fundraise_status(column='name', value=name)

    async def _select_fundraise_status(self, column: str, value: UUID | str) -> FundraiseStatus | None:
        self._log.debug(f'Getting FundraiseStatus with "{column}": "{value}" from the db.')
        q = select(FundraiseStatus).where(FundraiseStatus.__table__.columns[column] == value)
        result = await self.session.execute(q)
        return result.scalars().one_or_none()

    async def add_fundraise_status(self, fundraise_status: FundraiseStatusInputSchema) -> FundraiseStatus:
        """Add FundraiseStatus object to the database.

        Args:
            fundraise: FundraiseStatusInputSchema object.

        Returns:
        Newly created FundraiseStatus object.
        """
        return await self._add_fundraise_status(fundraise_status)

    async def _add_fundraise_status(self, fundraise_status: FundraiseStatusInputSchema) -> FundraiseStatus:
        db_fundraise_status = FundraiseStatus(**fundraise_status.dict())
        self.session.add(db_fundraise_status)
        await self.session.commit()
        await self.session.refresh(db_fundraise_status)
        self._log.debug(f'FundraiseStatus with name: "{db_fundraise_status.name}" successfully created.')
        return db_fundraise_status
