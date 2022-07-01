from uuid import UUID

from sqlalchemy import func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fundraisers.models import Fundraise
from fundraisers.schemas import FundraiseInputSchema, FundraiseIsDonatableUpdateSchema, FundraiseUpdateSchema
from utils.logging import setup_logging


class FundraiseDBService:

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

    async def get_fundraise_by_id(self, id_: UUID) -> Fundraise | None:
        """Get Fundraise object from database filtered by id.

        Args:
            id_: UUID of fundraise.

        Returns:
        single Fundraise object filtered by id.
        """
        return await self._get_fundraise_by_id(id_)

    async def _get_fundraise_by_id(self, id_: UUID) -> Fundraise | None:
        return await self._select_fundraise(column='id', value=id_)

    async def _select_fundraise(self, column: str, value: UUID | str) -> Fundraise | None:
        self._log.debug(f'Getting Fundraise with "{column}": "{value}" from the db.')
        q = select(Fundraise).where(Fundraise.__table__.columns[column] == value)
        result = await self.session.execute(q)
        return result.scalars().one_or_none()

    async def update_fundraise(self, id_: UUID, update_data: FundraiseUpdateSchema) -> Fundraise:
        """Updates Fundraise object in the database.

        Args:
            id_: UUID of fundraise.
            update_data: FundraiseUpdateSchema object.

        Returns:
        updated Fundraise object.
        """
        return await self._update_fundraise(id_, update_data)

    async def _update_fundraise(self, id_: UUID, update_data: FundraiseUpdateSchema) -> Fundraise:
        await self.session.execute(update(Fundraise).where(Fundraise.id == id_).values(**update_data.dict()))
        await self.session.commit()
        # Return updated fundraise.
        self._log.debug(f'Fundraise with id: "{id_}" successfully updated.')
        return await self._get_fundraise_by_id(id_=id_)

    async def delete_fundraise(self, fundraise: Fundraise) -> None:
        """Delete fundraise object from the database.

        Args:
            fundraise: Fundraise object.

        Returns:
        Nothing.
        """
        return await self._delete_fundraise(fundraise)

    async def _delete_fundraise(self, fundraise: Fundraise) -> None:
        await self.session.delete(fundraise)
        await self.session.commit()
        self._log.debug(f'Fundraise with id: "{fundraise.id}" successfully deleted.')

    async def update_fundraise_is_donatable_status(
            self, id_: UUID, update_data: FundraiseIsDonatableUpdateSchema
    ) -> Fundraise:
        """Updates Fundraise object 'is_donatable' field data in the db.

        Args:
            id_: UUID of a Fundaise object.
            update_data: Serialized FundraiseIsDonatableUpdateSchema object.

        Returns:
        Updated Fundraise object.
        """
        return await self._update_fundraise_is_donatable_status(id_, update_data)

    async def _update_fundraise_is_donatable_status(
            self, id_: UUID, update_data: FundraiseIsDonatableUpdateSchema
    ) -> Fundraise:
        await self.session.execute(update(Fundraise).where(Fundraise.id == id_).values(**update_data.dict()))
        await self.session.commit()
        # Return updated fundraise.
        self._log.debug(f'Fundraise with id: "{id_}" successfully updated "is_donatable" field.')
        return await self._get_fundraise_by_id(id_=id_)
