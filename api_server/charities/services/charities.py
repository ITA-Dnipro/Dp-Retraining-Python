# from typing import List
from uuid import UUID

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from charities.db_services import CharityDBService, EmployeeDBService, EmployeeRoleDBService
from charities.models import Charity
from charities.schemas import CharityInputSchema, CharityUpdateSchema, EmployeeDBSchema
from charities.services.commons import CharityCommonService
from charities.utils.jwt import jwt_charity_validator
from charities.utils.role_permissions import employee_role_validator
from common.constants.charities import CharityEmployeeRoleConstants
from common.constants.prepopulates import EmployeeRolePopulateData
from db import get_session
from users.services import UserService
from utils.logging import setup_logging
from utils.pagination import PaginationPage


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
        """Add a Charity object to the database.

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
        db_charity_employee_role = await self.employee_role_db_service.add_role_to_charity_employee(
            role=supervisor_role, charity_employee=db_charity_employee,
        )
        await self.charity_db_service.refresh_object(db_charity_employee_role)
        await self.charity_db_service.refresh_object(db_charity_employee)
        await self.charity_db_service.refresh_object(db_charity)
        return await self.get_charity_by_id(id_=db_charity.id)

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
        db_charity = await self.get_charity_by_id(id_)
        usernames = [employee.user.username for employee in db_charity.employees]
        if jwt_charity_validator(jwt_subject=jwt_subject, usernames=usernames):
            # Checking if currently authenticated employee have sufficient roles to perform charity update.
            for db_employee in db_charity.charity_employees:
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
                await self.charity_db_service.refresh_object(db_charity)
                return db_charity

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
        db_charity = await self.get_charity_by_id(id_)
        usernames = [employee.user.username for employee in db_charity.charity_employees]
        if jwt_charity_validator(jwt_subject=jwt_subject, usernames=usernames):
            # Checking if currently authenticated employee have sufficient roles to perform delete charity.
            for db_employee in db_charity.charity_employees:
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
