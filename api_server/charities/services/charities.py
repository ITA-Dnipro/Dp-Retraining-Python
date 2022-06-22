# from typing import List
from uuid import UUID

from fastapi import Depends, status

# from sqlalchemy import and_, delete, select, update
# from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from charities.db_services import CharityDBService, CharityEmployeeDBService, EmployeeDBService, EmployeeRoleDBService
from charities.models import Charity
from charities.schemas import CharityInputSchema, CharityUpdateSchema, EmployeeDBSchema
from charities.services.commons import CharityCommonService
# from charities.utils import check_permission_to_manage_charity, remove_nullable_params
from charities.utils.exceptions import CharityNotFoundError
from charities.utils.jwt import jwt_charity_validator
from charities.utils.role_permissions import employee_role_validator
from common.constants.charities import CharityEmployeeRoleConstants
from common.constants.prepopulates import EmployeeRolePopulateData
from common.exceptions.charities import CharityExceptionMsgs
from db import get_session
from users.models import User
from users.services import UserService
# from users.utils.exceptions import UserNotFoundError
from utils.logging import setup_logging
from utils.pagination import PaginationPage

# from sqlalchemy.orm.collections import InstrumentedList
# from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND


class CharityService(CharityCommonService):

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session)
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.charity_db_service = CharityDBService(session)
        self.user_service = UserService(session)
        self.employee_db_service = EmployeeDBService(session)
        self.employee_role_db_service = EmployeeRoleDBService(session)

    async def add_charity(self, charity: CharityInputSchema, jwt_subject: str) -> Charity:
        """Add Charity object to the database.

        Args:
            charity: CharityInputSchema object.
            jwt_subject: decoded jwt identity.

        Returns:
        Newly created Charity object.
        """
        return await self._add_charity(charity, jwt_subject)

    async def _add_charity(self, charity: CharityInputSchema, jwt_subject: str) -> Charity:
        db_user = await self.user_service.get_user_by_username(jwt_subject)
        db_employee = db_user.employee
        if not db_employee:
            employee = EmployeeDBSchema(user_id=db_user.id)
            db_employee = await self.employee_db_service.add_employee(employee)
        db_charity = await self.charity_db_service.add_charity(charity)
        db_charity_employee = await self.save_employee_to_charity(employee=db_employee, charity=db_charity)
        supervisor_role = await self.employee_role_db_service.get_employee_role_by_name(
            EmployeeRolePopulateData.SUPERVISOR.value
        )
        await self.employee_role_db_service.add_role_to_charity_employee(
            role=supervisor_role, charity_employee=db_charity_employee,
        )
        return await self.get_charity_by_id_with_relationships(id_=db_charity.id)

    async def get_charities(self, page: int, page_size: int) -> PaginationPage:
        """Get Charity objects from database.

        Args:
            page: number of result page.
            page_size: number of items per page.

        Returns:
        PaginationPage object with items as a list of Charity objects.
        """
        return await self._get_charities(page, page_size)

    async def _get_charities(self, page: int, page_size: int) -> PaginationPage:
        charities = await self.charity_db_service.get_charities(page, page_size)
        total_charities = await self.charity_db_service.get_total_charities()
        return PaginationPage(items=charities, page=page, page_size=page_size, total=total_charities)

    async def update_charity(self, id_: UUID, jwt_subject: str, update_data: CharityUpdateSchema) -> Charity:
        """Updates Charity object data in the db.

        Args:
            id_: UUID of a Charity object.
            jwt_subject: decoded jwt identity.
            update_data: Serialized CharityUpdateSchema object.
        Raise:
            CharityPermissionError in case of employee not present in charity's employee list.
            CharityEmployeeRolePermissionError in case employee
        Returns:
        Updated Charity object.
        """
        return await self._update_charity(id_, jwt_subject, update_data)

    async def _update_charity(self, id_: UUID, jwt_subject: str, update_data: CharityUpdateSchema) -> Charity:
        # Checking if currently authenticated user is in Charity employees list.
        db_charity = await self.get_charity_by_id_with_relationships(id_)
        usernames = [employee.user.username for employee in db_charity.employees]
        if jwt_charity_validator(jwt_subject=jwt_subject, usernames=usernames):
            # Checking if currently authenticated employee have sufficient roles to perform charity update.
            for db_employee in db_charity.employees:
                if db_employee.user.username == jwt_subject:
                    break
            db_employee_roles = [role for role in db_employee.roles]
            db_employee_role_names = [role.name for role in db_employee_roles]
            if employee_role_validator(
                    employee_roles=db_employee_role_names,
                    allowed_roles=CharityEmployeeRoleConstants.EDIT_CHARITY_ROLES.value,
            ):
                # Updating and refreshing Charity.
                await self.charity_db_service.update_charity(id_, update_data)
                return await self.charity_db_service.refresh_charity(db_charity)

    async def delete_charity(self, id_: UUID,  jwt_subject: str) -> None:
        """Delete Fundraise object from the database.

        Args:
            id_: UUID of a Charity object.
            jwt_subject: decoded jwt identity.

        Returns:
        Nothing.
        """
        return await self._delete_charity(id_, jwt_subject)

    async def _delete_charity(self, id_: UUID, jwt_subject: str) -> None:
        # Checking if currently authenticated user is in Charity employees list.
        db_charity = await self.get_charity_by_id_with_relationships(id_)
        usernames = [employee.user.username for employee in db_charity.employees]
        if jwt_charity_validator(jwt_subject=jwt_subject, usernames=usernames):
            # Checking if currently authenticated employee have sufficient roles to perform delete charity.
            for db_employee in db_charity.employees:
                if db_employee.user.username == jwt_subject:
                    break
            db_employee_roles = [role for role in db_employee.roles]
            db_employee_role_names = [role.name for role in db_employee_roles]
            if employee_role_validator(
                    employee_roles=db_employee_role_names,
                    allowed_roles=CharityEmployeeRoleConstants.DELETE_CHARITY_ROLES.value,
            ):
                # Deleting Charity.
                await self.charity_db_service.delete_charity(db_charity)


    # async def get_organisations_list(self) -> List[CharityOrganisation]:
    #     """
    #     Retrieves all charity organisations
    # 
    #     Args:
    # 
    #     Returns:
    #         list of CharityOrganisation objects.
    #     """
    #     return await self._get_organisations_list()
    # 
    # async def edit_organisation(self, org_id: UUID, org_schema: CharityUpdateSchema) -> CharityOrganisation:
    #     """
    #     Edit CharityOrganisation object.
    # 
    #     Args:
    #         org_id: id of organisation we want to edit
    #         org_schema: CharityInputSchema object.
    # 
    #     Returns:
    #         Edited CharityOrganisation object.
    #     """
    #     return await self._edit_organisation(org_id, org_schema)
    # 
    # async def delete_organisation(self, org_id: UUID) -> None:
    #     """
    #     Delete CharityOrganisation object.
    # 
    #     Args:
    #         org_id: id of organisation we want to delete.
    # 
    #     Returns:
    #     """
    #     return await self._delete_organisation(org_id)
    # 
    # async def add_manager(self, organisation_id: UUID, manager: AddManagerSchema) -> CharityUserAssociation:
    #     """
    #     Add CharityOrganisation object.
    # 
    #     Args:
    #         organisation_id: id of organisation we want to add manager.
    #         manager: AddManagerSchema object.
    # 
    #     Returns:
    #         CharityUserAssociation model object.
    #     """
    #     return await self._add_manager(organisation_id, manager)
    # 
    # async def show_charity_managers(self, organisation_id: UUID) -> InstrumentedList:
    #     """
    #     Retrieves list of users that related to definite organisations.
    # 
    #     Args:
    #         organisation_id: id of organisation we want to list of managers.
    # 
    #     Returns:
    #          InstrumentedList object.
    #     """
    #     return await self._get_managers_of_organisation(organisation_id)
    # 
    # async def delete_manager_from_organisation(self, organisation_id: UUID, user_id: UUID):
    #     """
    #     Deletes list of users that related to definite organisations.
    # 
    #     Args:
    #         organisation_id: id of organisation. User will be removed from organisation with this id.
    #         user_id: id of manager we want to delete from organisation.
    # 
    #     """
    #     return await self._delete_manager_from_organisation(organisation_id, user_id)
    # 
    # async def _get_user_by_id(self, user_id: UUID) -> User:
    #     try:
    #         user = (
    #             await self.session.execute(select(User).where(User.__table__.columns["id"] == user_id))).scalar_one()
    #     except NoResultFound:
    #         raise UserNotFoundError(status_code=HTTP_404_NOT_FOUND, detail="User with this id hasn't been found")
    #     return user
    # 
    # async def _get_organisations_list(self) -> List[CharityOrganisation]:
    #     return (await self.session.execute(select(CharityOrganisation)
    #                                        .order_by(CharityOrganisation.title))).scalars().all()
    # 
    # async def _get_managers_of_organisation(self, organisation_id) -> InstrumentedList:
    #     self.Authorize.jwt_required()
    #     organisation = await self._get_organisation_by_id(organisation_id)
    #     return organisation.users_association
    # 
    # async def _get_organisation_by_id(self, org_id: UUID) -> CharityOrganisation:
    #     charity = await self.charity_db_service.get_charity_by_id(org_id)
    #     if not charity:
    #         raise OrganisationHTTPException(
    #             status_code=HTTP_404_NOT_FOUND,
    #             detail="This organisation hasn't been found",
    #         )
    #     return charity
    # 
    # async def _check_is_supermanager_and_higher(self, user_id_to_check, organisation_id_to_check):
    #     """
    #     Checks if this user has permissions to manage organisations with supermanager rights.
    # 
    #     Args:
    #         user_id_to_check: id of user we want to check.
    # 
    #     Raises:
    #         OrganisationHTTPException: Permission denied
    #     """
    #     try:
    #         user_charity_relation_data = (await self.session.execute(
    #             select(CharityUserAssociation).where(and_(
    #                 CharityUserAssociation.users_id == user_id_to_check,
    #                 CharityUserAssociation.charity_id == organisation_id_to_check
    #             )))).scalar_one()
    #     except NoResultFound:
    #         raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
    #                                         detail="You do not have permission to perform this action")
    #     if not (user_charity_relation_data.is_supermanager or user_charity_relation_data.is_director):
    #         raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
    #                                         detail="You do not have permission to perform this action")
    # 
    # async def _check_is_director(self, user_id_to_check, organisation_id_to_check):
    #     """
    #     Checks if this user has permissions to manage organisations with director rights.
    # 
    #     Args:
    #         user_id_to_check: id of user we want to check.
    # 
    #     Raises:
    #         OrganisationHTTPException: Permission denied
    #     """
    #     try:
    #         charity_user_association_of_current_user = (await self.session.execute(
    #             select(CharityUserAssociation).where(and_(
    #                 CharityUserAssociation.users_id == user_id_to_check,
    #                 CharityUserAssociation.charity_id == organisation_id_to_check
    #             )))).scalar_one()
    #     except NoResultFound:
    #         raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
    #                                         detail="You do not have permission to perform this action")
    #     if not charity_user_association_of_current_user.is_director:
    #         raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
    #                                         detail="You do not have permission to perform this action")
    # 
    # async def _check_is_charity_member(self, org_id: UUID, current_user_id):
    #     """
    #     Checks if this user has permissions to manage organisations with director rights.
    # 
    #     Args:
    #         org_id: id of organisation. Pulls all users of organisation and check if this user is its member.
    # 
    #     Raises:
    #         OrganisationHTTPException: Permission denied
    #     """
    # 
    #     organisation = await self._get_organisation_by_id(org_id)
    #     users = organisation.users
    # 
    #     if not check_permission_to_manage_charity(users, current_user_id):
    #         raise OrganisationHTTPException(status_code=HTTP_403_FORBIDDEN,
    #                                         detail="You do not have permission to perform this action")
    # 
    # async def _add_manager(self, organisation_id: UUID, candidate: AddManagerSchema) -> CharityUserAssociation:
    #     self.Authorize.jwt_required()
    # 
    #     current_user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]
    #     await self._check_is_supermanager_and_higher(current_user_id, organisation_id)
    # 
    #     user = await self._get_user_by_id(candidate.user_id)
    #     organisation = await self._get_organisation_by_id(organisation_id)
    #     current_managers = organisation.users
    # 
    #     if user in current_managers:
    #         raise OrganisationHTTPException(status_code=HTTP_400_BAD_REQUEST, detail="This user is already manager")
    # 
    #     association = CharityUserAssociation()
    #     association.user = user
    #     association.charity = organisation
    #     association.is_supermanager = candidate.is_supermanager
    # 
    #     self.session.add(association)
    #     await self.session.commit()
    #     return association
    # 
    # async def _edit_organisation(self, org_id: UUID, org_schema: CharityUpdateSchema) -> CharityOrganisation:
    # 
    #     self.Authorize.jwt_required()
    #     current_user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]
    # 
    #     await self._check_is_charity_member(org_id, current_user_id)
    # 
    #     organisation_data = remove_nullable_params(org_schema.dict())
    # 
    #     await self.session.execute(update(CharityOrganisation).where(CharityOrganisation.id == org_id)
    #                                .values(**organisation_data))
    #     await self.session.commit()
    # 
    #     return await self._get_organisation_by_id(org_id)
    # 
    # async def _delete_organisation(self, org_id: UUID):
    #     self.Authorize.jwt_required()
    #     current_user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]
    # 
    #     await self._check_is_director(current_user_id, org_id)
    # 
    #     await self.session.execute(delete(CharityUserAssociation).where(CharityUserAssociation.charity_id == org_id))
    #     await self.session.delete(await self._get_organisation_by_id(org_id))
    #     await self.session.commit()
    # 
    # async def _delete_manager_from_organisation(self, organisation_id, user_id):
    #     self.Authorize.jwt_required()
    #     current_user_id = self.Authorize.get_raw_jwt()["user_data"]["id"]
    # 
    #     await self._check_is_director(current_user_id, organisation_id)
    #     await self.session.execute(delete(CharityUserAssociation).where(and_(
    #         CharityUserAssociation.users_id == user_id,
    #         CharityUserAssociation.charity_id == organisation_id
    #     )))
    #     await self.session.commit()
