from abc import ABCMeta
from typing import List
from uuid import UUID
import abc

from fastapi import Depends

from fastapi_jwt_auth import AuthJWT
from sqlalchemy import and_, delete, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.collections import InstrumentedList
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from charity.models import CharityOrganisation, CharityUserAssociation
from charity.schemas import AddManagerSchema, CharityInputSchema, CharityUpdateSchema
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
        return await self._get_managers_of_organisation(organisation_id)

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
    async def _get_managers_of_organisation(self, organisation_id: UUID) -> InstrumentedList:
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

    async def _get_user_by_id(self, user_id: UUID) -> User:
        try:
            user = (
                await self.session.execute(select(User).where(User.__table__.columns["id"] == user_id))).scalar_one()
        except NoResultFound:
            raise UserNotFoundError(status_code=HTTP_404_NOT_FOUND, detail="User with this id hasn't been found")
        return user

    async def _get_organisations_list(self) -> List[CharityOrganisation]:
        return (await self.session.execute(select(CharityOrganisation)
                                           .order_by(CharityOrganisation.title))).scalars().all()

    async def _get_managers_of_organisation(self, organisation_id) -> InstrumentedList:
        self.Authorize.jwt_required()
        organisation = await self._get_organisation_by_id(organisation_id)
        return organisation.users_association

    async def _get_organisation_by_id(self, org_id: UUID) -> CharityOrganisation:
        try:
            organisation = (await self.session.execute(select(CharityOrganisation)
                                                       .where(CharityOrganisation.id == org_id))).scalar_one()
        except NoResultFound:
            raise OrganisationHTTPException(status_code=HTTP_404_NOT_FOUND,
                                            detail="This organisation hasn't been found")
        return organisation

    async def _check_is_supermanager_and_higher(self, user_id_to_check):
        """
        Checks if this user has permissions to manage organisations with supermanager rights.

        Args:
            user_id_to_check: id of user we want to check.

        Raises:
            OrganisationHTTPException: Permission denied
        """
        try:
            user_charity_relation_data = (await self.session.execute(
                select(CharityUserAssociation).where(
                    CharityUserAssociation.users_id == user_id_to_check
                ))).scalar_one()
        except NoResultFound:
            raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
                                            detail="You do not have permission to perform this action")
        if not (user_charity_relation_data.is_supermanager or user_charity_relation_data.is_director):
            raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
                                            detail="You do not have permission to perform this action")

    async def _check_is_director(self, user_id_to_check):
        """
        Checks if this user has permissions to manage organisations with director rights.

        Args:
            user_id_to_check: id of user we want to check.

        Raises:
            OrganisationHTTPException: Permission denied
        """
        try:
            charity_user_association_of_current_user = (await self.session.execute(
                select(CharityUserAssociation).where(
                    CharityUserAssociation.users_id == user_id_to_check
                ))).scalar_one()
        except NoResultFound:
            raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
                                            detail="You do not have permission to perform this action")
        if not charity_user_association_of_current_user.is_director:
            raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
                                            detail="You do not have permission to perform this action")

    async def _check_is_charity_member(self, org_id: UUID, current_user_id):
        """
        Checks if this user has permissions to manage organisations with director rights.

        Args:
            org_id: id of organisation. Pulls all users of organisation and check if this user is its member.

        Raises:
            OrganisationHTTPException: Permission denied
        """

        organisation = await self._get_organisation_by_id(org_id)
        users = organisation.users

        if not check_permission_to_manage_charity(users, current_user_id):
            raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
                                            detail="You do not have permission to perform this action")

    async def _add_organisation(self, org: CharityInputSchema) -> CharityOrganisation:
        self.Authorize.jwt_required()
        organisation_data = org.dict()
        user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]
        organisation = CharityOrganisation(**organisation_data)
        association = CharityUserAssociation()
        user = await self._get_user_by_id(UUID(user_id))

        association.user = user
        association.is_supermanager = True
        association.is_director = True
        organisation.users_association.append(association)
        self.session.add(organisation)
        await self.session.commit()
        await self.session.refresh(organisation)
        return organisation

    async def _add_manager(self, organisation_id: UUID, candidate: AddManagerSchema) -> CharityUserAssociation:
        self.Authorize.jwt_required()

        current_user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]
        await self._check_is_supermanager_and_higher(current_user_id)

        user = await self._get_user_by_id(candidate.user_id)
        organisation = await self._get_organisation_by_id(organisation_id)
        current_managers = organisation.users

        if user in current_managers:
            raise OrganisationHTTPException(status_code=HTTP_400_BAD_REQUEST, detail="This user is already manager")

        association = CharityUserAssociation()
        association.user = user
        association.charity = organisation
        association.is_supermanager = candidate.is_supermanager

        self.session.add(association)
        await self.session.commit()
        return association

    async def _edit_organisation(self, org_id: UUID, org_schema: CharityUpdateSchema) -> CharityOrganisation:

        self.Authorize.jwt_required()
        current_user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]

        await self._check_is_charity_member(org_id, current_user_id)

        organisation_data = remove_nullable_params(org_schema.dict())

        await self.session.execute(update(CharityOrganisation).where(CharityOrganisation.id == org_id)
                                   .values(**organisation_data))
        await self.session.commit()

        return await self._get_organisation_by_id(org_id)

    async def _delete_organisation(self, org_id: UUID):
        self.Authorize.jwt_required()
        current_user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]

        await self._check_is_director(current_user_id)

        await self.session.execute(delete(CharityUserAssociation).where(CharityUserAssociation.charity_id == org_id))
        await self.session.delete(await self._get_organisation_by_id(org_id))
        await self.session.commit()

    async def _delete_manager_from_organisation(self, organisation_id, user_id):
        self.Authorize.jwt_required()
        current_user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]

        await self._check_is_director(current_user_id)
        await self.session.execute(delete(CharityUserAssociation)
                                   .where(
            and_(CharityUserAssociation.users_id == user_id, CharityUserAssociation.charity_id == organisation_id)))
        await self.session.commit()
