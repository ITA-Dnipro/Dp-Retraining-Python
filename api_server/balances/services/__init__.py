from typing import Union
from uuid import UUID
import abc

from fastapi import Depends, status

from fastapi_jwt_auth import AuthJWT
from sqlalchemy import update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from balances.models import Balance
from balances.schemas import BalanceInputSchema, BalanceUpdateSchema
from balances.utils.exceptions import BalanceNotFoundError, BalancePermissionError
from db import get_session
from utils.logging import setup_logging


class AbstractBalanceService(metaclass=abc.ABCMeta):

    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        Authorize: AuthJWT = Depends(),
    ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.Authorize = Authorize

    async def get_balances(self) -> list[Balance]:
        """Get Balance objects from database.

        Returns:
        list of Balance objects.
        """
        return await self._get_balances()

    async def get_balance_by_id(self, id_: str) -> Balance:
        """Get Balance object from database filtered by id.

        Args:
            id_: UUID of balance.

        Returns:
        single Balance object filtered by id.
        """
        return await self._get_balance_by_id(id_)

    async def add_balance(self, balance: BalanceInputSchema) -> Balance:
        """Add Balance object to the database.

        Args:
            balance: BalanceInputSchema object.

        Returns:
        newly created Balance object.
        """
        return await self._add_balance(balance)

    async def update_balance(self, id_: str, balance: BalanceUpdateSchema) -> Balance:
        """Updates Balance object in the database.

        Args:
            id_: UUID of balance.
            balance: BalanceUpdateSchema object.

        Returns:
        updated Balance object.
        """
        return await self._update_balance(id_, balance)

    async def delete_balance(self, id_: str) -> None:
        """Delete Balance object from the database.

        Args:
            id_: UUID of balance.

        Returns:
        Nothing.
        """
        return await self._delete_balance(id_)

    @abc.abstractclassmethod
    async def _get_balances(self) -> None:
        pass

    @abc.abstractclassmethod
    async def _get_balance_by_id(self, id_: str) -> None:
        pass

    @abc.abstractclassmethod
    async def _add_balance(self, balance: BalanceInputSchema) -> None:
        pass

    @abc.abstractclassmethod
    async def _update_balance(self, id_: str, balance: BalanceUpdateSchema) -> None:
        pass

    @abc.abstractclassmethod
    async def _delete_balance(self, id_: str) -> None:
        pass


class BalanceService(AbstractBalanceService):

    async def _get_balances(self) -> None:
        self._log.debug('Getting all balances from the db.')
        balances = await self.session.execute(select(Balance))
        return balances.scalars().all()

    async def _balance_exists(self, column: str, value: Union[UUID, str]) -> bool:
        balance = await self.session.execute(
            select(Balance).where(Balance.__table__.columns[column] == value))
        try:
            balance.one()
        except NoResultFound as err:
            err_msg = f"Balance with {column}: '{value}' not found."
            self._log.debug(err_msg)
            self._log.debug(err)
            raise BalanceNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return True

    async def _select_balance(self, column: str, value: Union[UUID, str]) -> None:
        balance_exists = await self._balance_exists(column=column, value=value)
        if balance_exists:
            balance = await self.session.execute(select(Balance).where(Balance.__table__.columns[column] == value))
            return balance.scalar_one()

    async def _get_balance_by_id(self, id_: str) -> None:
        self.Authorize.jwt_required()
        jwt_subject = self.Authorize.get_jwt_subject()
        from users.services import UserService
        user = await UserService(session=self.session)._get_user_by_username(username=jwt_subject)
        if user and user.balance_id == id_:
            self._log.debug(f'''Getting balance with id: "{id_}" from the db.''')
            balance = await self._select_balance(column='id', value=id_)
            return balance
        else:
            err_msg = f'''User don't have access to balance with id: "{id_}".'''
            self._log.debug(err_msg)
            raise BalancePermissionError(status_code=status.HTTP_403_FORBIDDEN, detail=err_msg)

    async def _add_balance(self, balance: BalanceInputSchema) -> None:
        balance = Balance(**balance.dict())
        self.session.add(balance)
        await self.session.commit()
        await self.session.refresh(balance)
        return balance

    async def _update_balance(self, id_: str, balance: BalanceUpdateSchema) -> None:
        balance_exists = await self._select_balance(column='id', value=id_)
        if balance_exists:
            # Updating balance.
            new_balance = balance_exists.amount + balance
            await self.session.execute(
                update(Balance).where(Balance.id == id_).values({'amount': new_balance}))
            await self.session.commit()

    async def _delete_balance(self, id_) -> None:
        balance = await self._select_balance(column='id', value=id_)
        if balance:
            from donations.services import DonationService
            from refills.services import RefillService
            donations = await DonationService(session=self.session).get_donations()
            for donation in donations:
                if donation.sender_id == balance.id or donation.recipient_id == balance.id:
                    await DonationService(session=self.session).delete_donation(id_=donation.id)
            refills = await RefillService(session=self.session).get_refills()
            for refill in refills:
                if refill.balance_id == balance.id:
                    await RefillService(session=self.session).delete_refill(id_=refill.id)
            # Deleting balance.
            await self.session.delete(balance)
            await self.session.commit()
            self._log.debug(f'''Balance with id: "{id_}" deleted.''')
