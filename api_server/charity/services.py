import abc
from abc import ABCMeta
from typing import List
from uuid import UUID

from fastapi import Depends

from fastapi_jwt_auth import AuthJWT
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from charity.models import CharityOrganisation, CharityUserAssociation
from charity.schemas import CharityInputSchema, CharityUpdateSchema
from charity.utils import check_permission_to_manage_charity, remove_nullable_params
from charity.utils.exceptions import OrganisationHTTPException
from db import get_session
from users.models import User
from users.utils.exceptions import UserNotFoundError
from utils.logging import setup_logging


class AbstractCharityService(metaclass=ABCMeta):

    def __init__(
            self,
            session: AsyncSession = Depends(get_session),
            authorize: AuthJWT = Depends(),
    ):
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.Authorize = authorize

    async def get_exact_organisation(self, org_id: UUID) -> CharityOrganisation:
        """
        Retrieves definite charity organisation.

        Args:
            org_id: id of organisation we want to retrieve
        Returns:
            CharityOrganisation object.
        """
        return await self._get_organisation_by_id(org_id)

    async def get_organisations_list(self) -> List[CharityOrganisation]:
        """
        Retrieves all charity organisations

        Args:

        Returns:
            list of CharityOrganisation objects.
        """
        return await self._get_organisations_list()

    async def add_organisation(self, org: CharityInputSchema) -> CharityOrganisation:
        """
        Add CharityOrganisation object to the database.

        Args:
            org: CharityInputSchema object.

        Returns:
            Newly created CharityOrganisation object.
        """
        return await self._add_organisation(org)

    async def edit_organisation(self, org_id: UUID, org_schema: CharityUpdateSchema) -> CharityOrganisation:
        """
        Edit CharityOrganisation object.

        Args:
            org_id: id of organisation we want to edit
            org_schema: CharityInputSchema object.

        Returns:
            Edited CharityOrganisation object.
        """
        return await self._edit_organisation(org_id, org_schema)

    async def delete_organisation(self, org_id: UUID) -> None:
        """
        Delete CharityOrganisation object.

        Args:
            org_id: id of organisation we want to delete.

        Returns:
        """
        return await self._delete_organisation(org_id)

    async def add_manager(self, organisation_id: UUID, manager: AddManagerSchema) -> CharityUserAssociation:
        """
        Delete CharityOrganisation object.

        Args:
            organisation_id: id of organisation we want to add manager.
            manager: AddManagerSchema object.

        Returns:
            CharityUserAssociation model object.
        """
        return await self._add_manager(organisation_id, manager)

    async def show_charity_managers(self, organisation_id: UUID) -> InstrumentedList:
        """
        Retrieves list of users that related to definite organisations.

        Args:
            organisation_id: id of organisation we want to list of managers.

        Returns:
             InstrumentedList object.
        """
        return await self._show_charity_managers(organisation_id)

    async def delete_manager_from_organisation(self, organisation_id: UUID, user_id: UUID):
        """
        Retrieves list of users that related to definite organisations.

        Args:
            organisation_id: id of organisation. User will be removed from organisation with this id.
            user_id: id of manager we want to delete from organisation.

        Returns:
             InstrumentedList object.
        """
        return await self._delete_manager_from_organisation(organisation_id, user_id)

    @abc.abstractmethod
    async def _show_charity_managers(self, organisation_id: UUID) -> InstrumentedList:
        pass

    @abc.abstractmethod
    async def _get_organisation_by_id(self, org_id: UUID) -> CharityOrganisation:
        pass

    @abc.abstractmethod
    async def _get_organisations_list(self) -> List[CharityOrganisation]:
        pass

    @abc.abstractmethod
    async def _add_organisation(self, org: CharityInputSchema) -> CharityOrganisation:
        pass

    @abc.abstractmethod
    async def _edit_organisation(self, org_id: UUID, org: CharityUpdateSchema) -> CharityOrganisation:
        pass

    @abc.abstractmethod
    async def _delete_organisation(self, org_id: UUID):
        pass

    @abc.abstractmethod
    async def _add_manager(self, organisation_id: UUID, manager: AddManagerSchema) -> CharityUserAssociation:
        pass

    @abc.abstractmethod
    async def _delete_manager_from_organisation(self, organisation_id, user_id):
        pass


class CharityService(AbstractCharityService):

    async def _get_user(self, user_id: UUID) -> User:
        try:
            user = await self.session.execute(select(User).where(User.__table__.columns["id"] == user_id))
        except NoResultFound:
            raise UserNotFoundError(status_code=HTTP_404_NOT_FOUND, detail="User with this id hasn't been found")
        return user.scalar_one()

    async def _add_organisation(self, org: CharityInputSchema) -> CharityOrganisation:
        self.Authorize.jwt_required()
        organisation_data = org.dict()
        user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]
        organisation = CharityOrganisation(**organisation_data)
        association = CharityUserAssociation()
        user = await self._get_user(UUID(user_id))

        association.user = user
        association.is_supermanager = True
        organisation.users_association.append(association)
        self.session.add(organisation)
        await self.session.commit()
        await self.session.refresh(organisation)
        return organisation

    async def _get_organisation_by_id(self, org_id: UUID) -> CharityOrganisation:
        try:
            organisation = (await self.session.execute(select(CharityOrganisation)
                                                       .where(CharityOrganisation.id == org_id))).scalar_one()
        except NoResultFound:
            raise OrganisationHTTPException(status_code=HTTP_404_NOT_FOUND,
                                            detail="This organisation hasn't been found")
        return organisation

    async def _get_charity_or_permission_error(self, org_id: UUID) -> CharityOrganisation:
        self.Authorize.jwt_required()
        current_user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]

        organisation = await self._get_organisation_by_id(org_id)
        users = organisation.users

        if not check_permission_to_manage_charity(users, current_user_id):
            raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
                                            detail="You do not have permission to perform this action")

        return organisation

    async def _edit_organisation(self, org_id: UUID, org_schema: CharityUpdateSchema) -> CharityOrganisation:

        await self._get_charity_or_permission_error(org_id)

        organisation_data = remove_nullable_params(org_schema.dict())

        await self.session.execute(update(CharityOrganisation).where(CharityOrganisation.id == org_id)
                                   .values(**organisation_data))
        await self.session.commit()

        return await self._get_organisation_by_id(org_id)

    async def _delete_organisation(self, org_id: UUID):
        organisation = await self._get_charity_or_permission_error(org_id)
        # future refactor: if we implement many managers on org, we should delete association table recursively
        await self.session.delete(organisation.users_association[0])
        await self.session.delete(organisation)
        await self.session.commit()

    async def _get_organisations_list(self) -> List[CharityOrganisation]:
        return (await self.session.execute(select(CharityOrganisation)
                                           .order_by(CharityOrganisation.title))).scalars().all()

    async def _add_manager(self, organisation_id: UUID, manager: AddManagerSchema) -> CharityUserAssociation:
        self.Authorize.jwt_required()
        organisation = await self._get_organisation_by_id(organisation_id)
        current_user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]
        current_user = await self._get_user(UUID(current_user_id))
        user = await self._get_user(manager.user_id)
        association = CharityUserAssociation()
        current_managers = organisation.users

        user_charity_relation_data = (await self.session.execute(
            select(CharityUserAssociation).where(
                CharityUserAssociation.users_id == current_user_id
            ))).scalar_one()

        if current_user not in current_managers or not user_charity_relation_data.is_supermanager:
            raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
                                            detail="You do not have permission to perform this action")
        if user in current_managers:
            raise OrganisationHTTPException(status_code=HTTP_400_BAD_REQUEST, detail="This user is already manager")

        association.user = user
        association.charity = organisation
        association.is_supermanager = manager.is_supermanager

        self.session.add(association)
        await self.session.commit()
        return association

    async def _show_charity_managers(self, organisation_id) -> InstrumentedList:
        self.Authorize.jwt_required()
        organisation = await self._get_organisation_by_id(organisation_id)
        return organisation.users_association

    async def _delete_manager_from_organisation(self, organisation_id, user_id):
        pass





