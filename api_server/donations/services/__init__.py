from typing import Union
from uuid import UUID
import abc

from fastapi import Depends, status

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from balances.services import BalanceService
from db import get_session
from donations.models import Donation
from donations.schemas import DonationInputSchema
from donations.utils.exceptions import DonationNotFoundError, DonationPermissionError
from users.services import UserService
from utils.logging import setup_logging


class AbstractDonationService(metaclass=abc.ABCMeta):

    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        Authorize: AuthJWT = Depends(),
    ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.Authorize = Authorize

    async def get_donations(self) -> list[Donation]:
        """Get donation objects from database.

        Returns:
        list of donation objects.
        """
        return await self._get_donations()

    async def get_donation_by_id(self, id_: str) -> Donation:
        """Get donation object from database filtered by id.

        Args:
            id_: UUID of donations.

        Returns:
        single donation object filtered by id.
        """
        return await self._get_donation_by_id(id_)

    async def add_donation(self, donation: DonationInputSchema) -> Donation:
        """Add donation object to the database.

        Args:
            donation: DonationInputSchema object.

        Returns:
        newly created Donation object.
        """
        return await self._add_donation(donation)

    async def delete_donation(self, id_: str) -> None:
        """Delete Donation object from the database.

        Args:
            id_: UUID of donation.

        Returns:
        Nothing.
        """
        return await self._delete_donation(id_)

    @abc.abstractclassmethod
    async def _get_donations(self) -> None:
        pass

    @abc.abstractclassmethod
    async def _get_donation_by_id(self, id_: str) -> None:
        pass

    @abc.abstractclassmethod
    async def _add_donation(self, donation: DonationInputSchema) -> None:
        pass

    @abc.abstractclassmethod
    async def _delete_donation(self, id_: str) -> None:
        pass


class DonationService(AbstractDonationService):

    async def _get_donations(self) -> None:
        self._log.debug('Getting all donations from the db.')
        donations = await self.session.execute(select(Donation))
        return donations.scalars().all()

    async def _donation_exists(self, column: str, value: Union[UUID, str]) -> bool:
        donation = await self.session.execute(select(Donation).where(Donation.__table__.columns[column] == value))
        try:
            donation.one()
        except NoResultFound as err:
            err_msg = f"Donation with {column}: '{value}' not found."
            self._log.debug(err_msg)
            self._log.debug(err)
            raise DonationNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return True

    async def _select_donation(self, column: str, value: Union[UUID, str]) -> None:
        donation_exists = await self._donation_exists(column=column, value=value)
        if donation_exists:
            donation = await self.session.execute(select(Donation).where(Donation.__table__.columns[column] == value))
            return donation.scalar_one()

    async def _get_donation_by_id(self, id_: str) -> None:
        self._log.debug(f'''Getting donation with id: "{id_}" from the db.''')
        donation = await self._select_donation(column='id', value=id_)
        return donation

    async def add_donation(self, donation: DonationInputSchema) -> None:
        self.Authorize.jwt_required()
        jwt_subject = self.Authorize.get_jwt_subject()
        user = await UserService(session=self.session)._get_user_by_username(
            username=jwt_subject
        )
        if user:
            user_balance = await BalanceService(
                session=self.session, Authorize=self.Authorize
            ).get_balance_by_id(id_=user.balance_id)
            if donation.amount <= user_balance.amount or donation.amount <= 0:
                donation.sender_id = user.balance_id
                return await self._add_donation(donation)
        err_msg = f'''Current user don't have enough cash at balance with id: "{user.balance_id}".'''
        self._log.debug(err_msg)
        raise DonationPermissionError(
            status_code=status.HTTP_403_FORBIDDEN, detail=err_msg
        )

    async def _add_donation(self, donation: DonationInputSchema) -> None:
        donation = Donation(**donation.dict())
        self.session.add(donation)
        await self.session.commit()
        await self.session.refresh(donation)
        await BalanceService(
            session=self.session
        ).update_balance(donation.recipient_id, donation.amount)
        await BalanceService(
            session=self.session
        ).update_balance(donation.sender_id, -donation.amount)
        return donation

    async def _delete_donation(self, id_) -> None:
        donation = await self._select_donation(column='id', value=id_)
        if donation:
            # Deleting donation.
            await self.session.delete(donation)
            await self.session.commit()
            self._log.debug(f'''Donation with id: "{id_}" deleted.''')
