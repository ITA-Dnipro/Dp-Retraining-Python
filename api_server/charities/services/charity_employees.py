from uuid import UUID

from fastapi import Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from charities.db_services import CharityEmployeeDBService, EmployeeDBService, EmployeeRoleDBService
from charities.models import Charity, Employee
from charities.schemas import EmployeeDBSchema, EmployeeInputSchema
from charities.services.commons import CharityCommonService
from charities.utils.exceptions import CharityEmployeeNotFoundError, CharityNonRemovableEmployeeError
from charities.utils.jwt import jwt_charity_validator
from charities.utils.role_permissions import (
    employee_role_validator,
    get_allowed_role_for_employee_role,
    get_allowed_roles_for_employee_roles,
)
from common.constants.charities import CharityEmployeeAllowedRolesConstants, CharityEmployeeServiceConstants
from common.exceptions.charities import CharityEmployeesExceptionMsgs
from db import get_session
from users.services import UserService
from utils.logging import setup_logging


class CharityEmployeeService(CharityCommonService):

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session)
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.charity_employee_db_service = CharityEmployeeDBService(session)
        self.user_service = UserService(session)
        self.employee_db_service = EmployeeDBService(session)
        self.employee_role_db_service = EmployeeRoleDBService(session)

    async def add_employee_to_charity(
            self, charity_id: UUID, jwt_subject: str, employee_data: EmployeeInputSchema,
    ) -> Employee:
        """Add Employee to Charity object in the database via many-to-many relationship.

        Args:
            charity_id: UUID of charity.
            jwt_subject: decoded jwt identity.
            employee_data: Serialized EmployeeInputSchema object.

        Returns:
        Employee added to Charity via many-to-many relationship.
        """
        return await self._add_employee_to_charity(charity_id, jwt_subject, employee_data)

    async def _add_employee_to_charity(
            self, charity_id: UUID, jwt_subject: str, employee_data: EmployeeInputSchema,
    ) -> Employee:
        # Getting allowed roles for new employee role.
        allowed_roles = get_allowed_role_for_employee_role(
            role_name=employee_data.role,
            allowed_roles=CharityEmployeeAllowedRolesConstants.ADD_EMPLOYEE_ROLES_MAPPING.value,
        )
        # Checking if currently authenticated user is in Charity employees list.
        db_charity = await self.get_charity_by_id(charity_id)
        db_charity_employee_usernames = [employee.user.username for employee in db_charity.employees]
        if jwt_charity_validator(jwt_subject=jwt_subject, usernames=db_charity_employee_usernames):
            # Checking if currently authenticated employee have sufficient roles to add employee with role.
            for current_db_employee in db_charity.charity_employees:
                if current_db_employee.user.username == jwt_subject:
                    break
            current_db_employee_role_names = [role.name for role in current_db_employee.roles]
            if employee_role_validator(
                    employee_roles=current_db_employee_role_names,
                    allowed_roles=allowed_roles,
            ):
                # Using already created Employee or creating a new one.
                new_employee_db_user = await self.user_service.get_user_by_email(employee_data.user_email)
                new_db_employee = new_employee_db_user.employee
                if not new_db_employee:
                    employee = EmployeeDBSchema(user_id=new_employee_db_user.id)
                    new_db_employee = await self.employee_db_service.add_employee(employee)
                # Adding new employee to charity.
                new_db_charity_employee = await self.save_employee_to_charity(new_db_employee, db_charity)
                new_employee_role = await self.employee_role_db_service.get_employee_role_by_name(
                    name=employee_data.role,
                )
                # Adding EmployeeRole to charity employee.
                await self.employee_role_db_service.add_role_to_charity_employee(
                    role=new_employee_role,
                    charity_employee=new_db_charity_employee,
                )
                # Refreshing and returning new_db_charity_employee with roles.
                await self.charity_db_service.refresh_object(new_db_charity_employee)
                return new_db_charity_employee

    async def get_charity_employees(self, charity_id: UUID) -> list[Employee]:
        """Get Charity's Employee objects from the database.

        Args:
            charity_id: UUID of a Charity object.

        Returns:
        list of charity's Employee objects.
        """
        return await self._get_charity_employees(charity_id)

    async def _get_charity_employees(self, charity_id: UUID) -> list[Employee]:
        db_charity = await self.get_charity_by_id(charity_id)
        return db_charity.charity_employees

    async def get_charity_employee_by_id(self, charity_id: UUID, employee_id: UUID) -> Employee:
        """Get Charity's Employee object from the database filtered by id.

        Args:
            charity_id: UUID of a Charity object.
            employee_id: UUID of an Employee object.

        Returns:
        Single charity's Employee object filtered by id.
        """
        return await self._get_charity_employee_by_id(charity_id, employee_id)

    async def _get_charity_employee_by_id(self, charity_id: UUID, employee_id: UUID) -> Employee:
        db_charity = await self.get_charity_by_id(charity_id)
        return await self.get_employee_from_charity_by_id(db_charity, employee_id)

    async def get_employee_from_charity_by_id(self, charity: Charity, employee_id: UUID) -> Employee:
        """Get Employee object by id from 'Charity.employees' collection.

        Args:
            charity: Charity object.
            employee_id: UUID of an Employee object.

        Raise:
            CharityEmployeeNotFoundError in case employee not present in 'Charity.employees' collection.

        Returns:
        Single charity's Employee object filtered by id.
        """
        return await self._get_employee_from_charity_by_id(charity, employee_id)

    async def _get_employee_from_charity_by_id(self, charity: Charity, employee_id: UUID) -> Employee:
        for employee in charity.charity_employees:
            if employee.id == employee_id:
                break
        else:
            err_msg = CharityEmployeesExceptionMsgs.EMPLOYEE_NOT_FOUND.value.format(
                field_name='id',
                field_value=employee_id,
                charity_id=charity.id,
            )
            self._log.debug(err_msg)
            raise CharityEmployeeNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return employee

    async def remove_employee_from_charity(self, charity_id: UUID, employee_id: UUID, jwt_subject: str) -> dict:
        """Removes Employee from Charity.

        Args:
            charity_id: UUID of a Charity object.
            employee_id: UUID of an Employee object.
            jwt_subject: decoded jwt identity.

        Returns:
        dict with successful employee removal message.
        """
        return await self._remove_employee_from_charity(charity_id, employee_id, jwt_subject)

    async def _remove_employee_from_charity(self, charity_id: UUID, employee_id: UUID, jwt_subject: str) -> dict:
        # Checking if currently authenticated user is in Charity employees list.
        db_charity = await self.get_charity_by_id(charity_id)
        db_charity_employee_usernames = [employee.user.username for employee in db_charity.charity_employees]
        if jwt_charity_validator(jwt_subject=jwt_subject, usernames=db_charity_employee_usernames):
            # Checking if currently authenticated employee have sufficient roles to perform action.
            authenticated_employee = await self.get_employee_from_charity_by_username(db_charity, jwt_subject)
            authenticated_employee_role_names = [role.name for role in authenticated_employee.roles]
            # Getting allowed roles for employee_to_delete roles.
            employee_to_delete = await self.get_employee_from_charity_by_id(db_charity, employee_id)
            employee_to_delete_role_names = [role.name for role in employee_to_delete.roles]
            employee_to_delete_allowed_roles = get_allowed_roles_for_employee_roles(
                roles=employee_to_delete_role_names,
                allowed_roles=CharityEmployeeAllowedRolesConstants.DELETE_EMPLOYEE_ROLES_MAPPING.value,
            )
            if employee_role_validator(
                    employee_roles=authenticated_employee_role_names,
                    allowed_roles=employee_to_delete_allowed_roles,
            ):
                # Checking if Charity have at least one Employee with supervisor role.
                total_supervisors_in_charity = await self.count_employee_role_in_charity(
                    charity=db_charity,
                    role_name=CharityEmployeeAllowedRolesConstants.SUPERVISOR.value,
                )
                employee_to_delete_is_supervisor = await self.employee_has_role(
                    employee=employee_to_delete,
                    role_name=CharityEmployeeAllowedRolesConstants.SUPERVISOR.value,
                )
                if total_supervisors_in_charity < 2 and employee_to_delete_is_supervisor:
                    err_msg = CharityEmployeesExceptionMsgs.EMPLOYEE_NON_REMOVABLE.value.format(
                        employee_role=CharityEmployeeAllowedRolesConstants.SUPERVISOR.value,
                        charity_id=db_charity.id,
                        role_count=total_supervisors_in_charity,
                    )
                    self._log.debug(err_msg)
                    raise CharityNonRemovableEmployeeError(status_code=status.HTTP_403_FORBIDDEN, detail=err_msg)
                # Removing Employee from Charity.employees.
                await self.charity_employee_db_service.remove_employee_from_charity(
                    db_charity,
                    employee_to_delete.employee,
                )
                CharityEmployeeServiceConstants.SUCCESSFUL_EMPLOYEE_REMOVAL_MSG.value['message'] = (
                    CharityEmployeeServiceConstants.SUCCESSFUL_EMPLOYEE_REMOVAL_MSG.value['message'].format(
                        charity_id=db_charity.id,
                        employee_id=employee_to_delete.id,
                    )
                )
                return CharityEmployeeServiceConstants.SUCCESSFUL_EMPLOYEE_REMOVAL_MSG.value

    async def get_employee_from_charity_by_username(self, charity: Charity, username: str) -> Employee:
        """Get Employee object by 'User.username' from 'Charity.employees' collection.

        Args:
            charity: Charity object.
            username: User username.

        Raise:
            CharityEmployeeNotFoundError in case employee not present in 'Charity.employees' collection.

        Returns:
        Single charity's Employee object filtered by User.username.
        """
        return await self._get_employee_from_charity_by_username(charity, username)

    async def _get_employee_from_charity_by_username(self, charity: Charity, username: str) -> Employee:
        for employee in charity.charity_employees:
            if employee.user.username == username:
                break
        else:
            err_msg = CharityEmployeesExceptionMsgs.EMPLOYEE_NOT_FOUND.value.format(
                field_name='username',
                field_value=username,
                charity_id=charity.id,
            )
            self._log.debug(err_msg)
            raise CharityEmployeeNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return employee
