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
from refills.models import Refill
from refills.schemas import RefillInputSchema
from refills.utils.exceptions import RefillNotFoundError, RefillPermissionError
from users.services import UserService
from utils.logging import setup_logging


class AbstractRefillService(metaclass=abc.ABCMeta):

    def __init__(
            self,
            session: AsyncSession = Depends(get_session),
            Authorize: AuthJWT = Depends(),
    ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.Authorize = Authorize

    async def get_refills(self) -> list[Refill]:
        """Get Refill objects from database.

        Returns:
        list of Refill objects.
        """
        return await self._get_refills()

    async def get_refill_by_id(self, id_: str) -> Refill:
        """Get Refill object from database filtered by id.

        Args:
            id_: UUID of refills.

        Returns:
        single Refill object filtered by id.
        """
        return await self._get_refill_by_id(id_)

    async def add_refill(self, refill: RefillInputSchema) -> Refill:
        """Add Refill object to the database.

        Args:
            refill: RefillInputSchema object.

        Returns:
        newly created Refill object.
        """
        return await self._add_refill(refill)

    async def delete_refill(self, id_: str) -> None:
        """Delete refill object from the database.

        Args:
            id_: UUID of refill.

        Returns:
        Nothing.
        """
        return await self._delete_refill(id_)

    @abc.abstractclassmethod
    async def _get_refills(self) -> None:
        pass

    @abc.abstractclassmethod
    async def _get_refill_by_id(self, id_: str) -> None:
        pass

    @abc.abstractclassmethod
    async def _add_refill(self, refill: RefillInputSchema) -> None:
        pass

    @abc.abstractclassmethod
    async def _delete_refill(self, id_: str) -> None:
        pass


class RefillService(AbstractRefillService):

    async def _get_refills(self) -> None:
        self._log.debug('Getting all users refills from the db.')
        refills = await self.session.execute(select(Refill))
        return refills.scalars().all()

    async def _refill_exists(self, column: str, value: Union[UUID, str]) -> bool:
        refill = await self.session.execute(
            select(Refill).where(Refill.__table__.columns[column] == value))
        try:
            refill.one()
        except NoResultFound as err:
            err_msg = f"Refill with {column}: '{value}' not found."
            self._log.debug(err_msg)
            self._log.debug(err)
            raise RefillNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return True

    async def _select_refill(self, column: str, value: Union[UUID, str]) -> None:
        refill_exists = await self._refill_exists(column=column, value=value)
        if refill_exists:
            refill = await self.session.execute(
                select(Refill).where(Refill.__table__.columns[column] == value))
            return refill.scalar_one()

    async def _get_refill_by_id(self, id_: str) -> None:
        self._log.debug(f'''Getting refill with id: "{id_}" from the db.''')
        self.Authorize.jwt_required()
        jwt_subject = self.Authorize.get_jwt_subject()
        user = await UserService(session=self.session).get_user_by_username(username=jwt_subject)
        if user:
            refill = await self._select_refill(column='id', value=id_)
            if refill.balance_id == user.balance_id:
                return refill
        err_msg = f'''User don't have access to balance with id: "{id_}".'''
        self._log.debug(err_msg)
        raise RefillPermissionError(status_code=status.HTTP_403_FORBIDDEN, detail=err_msg)

    async def add_refill(self, refill: RefillInputSchema) -> None:
        self.Authorize.jwt_required()
        jwt_subject = self.Authorize.get_jwt_subject()
        user = await UserService(session=self.session).get_user_by_username(username=jwt_subject)
        refill.balance_id = user.balance_id
        return await self._add_refill(refill)

    async def _add_refill(self, refill: RefillInputSchema) -> None:
        refill = Refill(**refill.dict())
        self.session.add(refill)
        await self.session.commit()
        await self.session.refresh(refill)
        await BalanceService(session=self.session, Authorize=self.Authorize).update_balance(
            refill.balance_id, refill.amount)
        return refill

    async def _delete_refill(self, id_) -> None:
        refill = await self._select_refill(column='id', value=id_)
        if refill:
            # Deleting refill.
            await self.session.delete(refill)
            await self.session.commit()
            self._log.debug(f'''Refill with id: "{id_}" deleted.''')
