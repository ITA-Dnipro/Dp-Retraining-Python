from abc import ABCMeta
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

    async def add_organisation(self, org: CharityInputSchema):
        """
        Add CharityOrganisation object to the database.

        Args:
            org: CharityInputSchema object.

        Returns:
            Newly created CharityOrganisation object.
        """
        return await self._add_organisation(org)

    async def edit_organisation(self, org_id, org_schema: CharityUpdateSchema):
        """
        Edit CharityOrganisation object.

        Args:
            org_id: id of organisation we want to edit
            org_schema: CharityInputSchema object.

        Returns:
            Edited CharityOrganisation object.
        """
        return await self._edit_organisation(org_id, org_schema)

    async def delete_organisation(self, org_id):
        """
        Delete CharityOrganisation object.

        Args:
            org_id: id of organisation we want to delete.

        Returns:
            Deleted CharityOrganisation object.
        """
        return await self._delete_organisation(org_id)

    @classmethod
    async def _add_organisation(cls, org):
        pass

    @classmethod
    async def _edit_organisation(cls, org_id, org):
        pass

    @classmethod
    async def _delete_organisation(cls, org_id):
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
        user_id = organisation_data.pop("user_id")
        organisation = CharityOrganisation(**organisation_data)
        association = CharityUserAssociation()
        user = await self._get_user(user_id)

        association.user = user
        organisation.users_association.append(association)
        self.session.add(organisation)
        await self.session.commit()
        await self.session.refresh(organisation)
        return organisation

    async def _get_organisation_by_id(self, org_id: str) -> CharityOrganisation:
        try:
            organisation = (await self.session.execute(select(CharityOrganisation)
                                                       .where(CharityOrganisation.id == org_id))).scalar_one()
        except NoResultFound:
            raise OrganisationHTTPException(status_code=HTTP_404_NOT_FOUND,
                                            detail="This organisation hasn't been found")
        return organisation

    async def _get_charity_or_permission_error(self, org_id: str) -> CharityOrganisation:
        self.Authorize.jwt_required()
        current_user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]

        organisation = await self._get_organisation_by_id(org_id)
        users = organisation.users

        if not check_permission_to_manage_charity(users, current_user_id):
            raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
                                            detail="You do not have permission to perform this action")

        return organisation

    async def _edit_organisation(self, org_id: str, org_schema: CharityUpdateSchema):

        await self._get_charity_or_permission_error(org_id)

        organisation_data = remove_nullable_params(org_schema.dict())

        await self.session.execute(update(CharityOrganisation).where(CharityOrganisation.id == org_id)
                                   .values(**organisation_data))
        await self.session.commit()

        return await self._get_organisation_by_id(org_id)

    async def _delete_organisation(self, org_id: str):
        organisation = await self._get_charity_or_permission_error(org_id)
        # future refactor: if we implement many managers on org, we should delete association table recursively
        await self.session.delete(organisation.users_association[0])
        await self.session.delete(organisation)
        await self.session.commit()
