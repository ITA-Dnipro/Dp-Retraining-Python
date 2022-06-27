from uuid import UUID

from fastapi import Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from charities.db_services import EmployeeRoleDBService
from charities.models import Employee, EmployeeRole
from charities.schemas import EmployeeRoleInputSchema
from charities.services.charity_employees import CharityEmployeeService
from charities.services.commons import CharityCommonService
from charities.utils.exceptions import (
    CharityEmployeeRoleDuplicateError,
    EmployeeNonRemovableEmployeeRoleError,
    EmployeeRoleNotFoundError,
)
from charities.utils.role_permissions import (
    employee_role_validator,
    get_allowed_role_for_employee_role,
    get_allowed_roles_for_employee_roles,
)
from common.constants.charities import CharityEmployeeAllowedRolesConstants, EmployeeRoleServiceConstants
from common.exceptions.charities import EmployeeRolesExceptionMsgs
from db import get_session
from utils.logging import setup_logging


class EmployeeRoleService(CharityCommonService):

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session)
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.charity_employee_service = CharityEmployeeService(session)
        self.employee_role_db_service = EmployeeRoleDBService(session)

    async def get_employee_roles(self, charity_id: UUID, employee_id: UUID) -> list[EmployeeRole]:
        """Get employee's EmployeeRole objects from the database.

        Args:
            charity_id: UUID of charity.
            employee_id: UUID of employee.

        Returns:
        list of employee's EmployeeRole objects.
        """
        return await self._get_employee_roles(charity_id, employee_id)

    async def _get_employee_roles(self, charity_id: UUID, employee_id: UUID) -> list[EmployeeRole]:
        db_charity = await self.get_charity_by_id_with_relationships(charity_id)
        db_charity_employee = await self.charity_employee_service.get_employee_from_charity_by_id(
            db_charity,
            employee_id,
        )
        return db_charity_employee.roles

    async def get_employee_role_by_id(self, charity_id: UUID, employee_id: UUID, role_id: UUID) -> EmployeeRole:
        """Get employee's EmployeeRole object from the database filtered by id.

        Args:
            charity_id: UUID of charity.
            employee_id: UUID of employee.
            role_id: UUID of EmployeeRole.

        Returns:
        Single employee's EmployeeRole object filtered by id.
        """
        return await self._get_employee_role_by_id(charity_id, employee_id, role_id)

    async def _get_employee_role_by_id(self, charity_id: UUID, employee_id: UUID, role_id: UUID) -> EmployeeRole:
        db_charity = await self.get_charity_by_id_with_relationships(charity_id)
        db_charity_employee = await self.charity_employee_service.get_employee_from_charity_by_id(
            db_charity,
            employee_id,
        )
        return await self.get_role_from_employee_by_id(db_charity_employee, role_id)

    async def get_role_from_employee_by_id(self, employee: Employee, role_id: UUID) -> EmployeeRole:
        """Get EmployeeRole object from 'Employee.roles' collection filtered by id.

        Args:
            employee: Employee object.
            role_id: UUID of a EmployeeRole object.

        Raise:
            EmployeeRoleNotFoundError in case EmployeeRole not present in 'Employee.roles' collection.

        Returns:
        Single employee's EmployeeRole object filtered by id.
        """
        return await self._get_role_from_employee_by_id(employee, role_id)

    async def _get_role_from_employee_by_id(self, employee: Employee, role_id: UUID) -> EmployeeRole:
        for role in employee.roles:
            if role.id == role_id:
                break
        else:
            err_msg = EmployeeRolesExceptionMsgs.ROLE_NOT_FOUND_IN_EMPLOYEE.value.format(
                role_id=role_id,
                employee_id=employee.id,
            )
            self._log.debug(err_msg)
            raise EmployeeRoleNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return role

    async def add_role_to_employee(
            self, charity_id: UUID, employee_id: UUID, jwt_subject: str, role_data: EmployeeRoleInputSchema,
    ) -> EmployeeRole:
        """Add Employee to Charity object in the database via many-to-many relationship.

        Args:
            charity_id: UUID of charity.
            employee_id: UUID of employee.
            jwt_subject: decoded jwt identity.
            role_data: Serialized EmployeeRoleInputSchema object.

        Returns:

        """
        return await self._add_role_to_employee(charity_id, employee_id, jwt_subject, role_data)

    async def _add_role_to_employee(
            self, charity_id: UUID, employee_id: UUID, jwt_subject: str, role_data: EmployeeRoleInputSchema,
    ) -> EmployeeRole:
        db_charity = await self.get_charity_by_id_with_relationships(charity_id)
        employee_to_add_role = await self.charity_employee_service.get_employee_from_charity_by_id(
            db_charity,
            employee_id,
        )
        # Checking if role already added to employee.
        employee_role_already_added_to_employee = await self.employee_has_role(
            employee=employee_to_add_role,
            role_name=role_data.name,
        )
        if employee_role_already_added_to_employee:
            err_msg = EmployeeRolesExceptionMsgs.ROLE_ALREADY_ADDED_TO_EMPLOYEE.value.format(
                field_name='name',
                field_value=role_data.name,
                employee_id=employee_to_add_role.id,
            )
            self._log.debug(err_msg)
            raise CharityEmployeeRoleDuplicateError(status_code=status.HTTP_400_BAD_REQUEST, detail=err_msg)
        # Checking if currently authenticated employee have sufficient roles to perform action.
        authenticated_employee = await self.charity_employee_service.get_employee_from_charity_by_username(
            db_charity,
            jwt_subject,
        )
        authenticated_employee_role_names = [role.name for role in authenticated_employee.roles]
        # Getting allowed roles for role name from payload.
        incoming_role_allowed_roles = get_allowed_role_for_employee_role(
            role_name=role_data.name,
            allowed_roles=CharityEmployeeAllowedRolesConstants.ADD_EMPLOYEE_ROLES_MAPPING.value,
        )
        if employee_role_validator(
                employee_roles=authenticated_employee_role_names,
                allowed_roles=incoming_role_allowed_roles,
        ):
            new_employee_role = await self.get_employee_role_by_name(name=role_data.name)
            charity_employee_to_add_role = await self.charity_employee_service.get_charity_employee_by_charity_and_employee_id( # noqa
                charity_id,
                employee_id,
            )
            await self.employee_role_db_service.add_role_to_charity_employee(
                role=new_employee_role,
                charity_employee=charity_employee_to_add_role,
            )
            return new_employee_role

    async def get_employee_role_by_name(self, name: str) -> EmployeeRole:
        """Get EmployeeRole object from database filtered by name.

        Args:
            name: of employee role.

        Returns:
        single EmployeeRole object filtered by name.
        """
        return await self._get_employee_role_by_name(name)

    async def _get_employee_role_by_name(self, name: str) -> EmployeeRole:
        employee_role = await self.employee_role_db_service.get_employee_role_by_name(name)
        if not employee_role:
            err_msg = EmployeeRolesExceptionMsgs.ROLE_NOT_FOUND.value.format(
                field_name='name',
                field_value=name,
            )
            self._log.debug(err_msg)
            raise EmployeeRoleNotFoundError(status_code=status.HTTP_404_NOT_FOUND, detail=err_msg)
        return employee_role

    async def remove_role_from_employee(
            self, charity_id: UUID, employee_id: UUID, role_id: UUID, jwt_subject: str,
    ) -> dict:
        """Removes EmployeeRole for 'Employee.roles' collection.

        Args:
            charity_id: UUID of charity.
            employee_id: UUID of employee.
            role_id: UUID of EmployeeRole.
            jwt_subject: decoded jwt identity.

        Returns:
        dict with successful EmployeeRole removal message.
        """
        return await self._remove_role_from_employee(charity_id, employee_id, role_id, jwt_subject)

    async def _remove_role_from_employee(
            self, charity_id: UUID, employee_id: UUID, role_id: UUID, jwt_subject: str,
    ) -> dict:
        db_charity = await self.get_charity_by_id_with_relationships(charity_id)
        # Checking if currently authenticated employee have sufficient roles to perform action.
        authenticated_employee = await self.charity_employee_service.get_employee_from_charity_by_username(
            db_charity,
            jwt_subject,
        )
        authenticated_employee_role_names = [role.name for role in authenticated_employee.roles]
        # Getting allowed roles for employee_to_remove_role.
        employee_to_remove_role = await self.charity_employee_service.get_employee_from_charity_by_id(
            db_charity,
            employee_id,
        )
        employee_to_remove_role_role_names = [role.name for role in employee_to_remove_role.roles]
        employee_to_remove_role_allowed_roles = get_allowed_roles_for_employee_roles(
            roles=employee_to_remove_role_role_names,
            allowed_roles=CharityEmployeeAllowedRolesConstants.DELETE_EMPLOYEE_ROLES_MAPPING.value,
        )
        if employee_role_validator(
                employee_roles=authenticated_employee_role_names,
                allowed_roles=employee_to_remove_role_allowed_roles,
        ):
            role_to_remove = await self.get_role_from_employee_by_id(employee=employee_to_remove_role, role_id=role_id)
            # Checking if Charity have at least one Employee with supervisor role.
            total_supervisors_in_charity = await self.count_employee_role_in_charity(
                charity=db_charity,
                role_name=CharityEmployeeAllowedRolesConstants.SUPERVISOR.value,
            )
            employee_role_to_remove_is_supervisor = await self.employee_has_role(
                employee=employee_to_remove_role,
                role_name=CharityEmployeeAllowedRolesConstants.SUPERVISOR.value,
            )
            if total_supervisors_in_charity < 2 and employee_role_to_remove_is_supervisor:
                err_msg = EmployeeRolesExceptionMsgs.EMPLOYEE_ROLE_NON_REMOVABLE_LAST_SUPERVISOR.value.format(
                    employee_role=CharityEmployeeAllowedRolesConstants.SUPERVISOR.value,
                    employee_id=employee_to_remove_role.id,
                    role_count=total_supervisors_in_charity,
                )
                self._log.debug(err_msg)
                raise EmployeeNonRemovableEmployeeRoleError(status_code=status.HTTP_403_FORBIDDEN, detail=err_msg)
            # Checking if employee removing his only role.
            total_employee_to_remove_roles = len(employee_to_remove_role.roles)
            if total_employee_to_remove_roles < 2:
                err_msg = EmployeeRolesExceptionMsgs.EMPLOYEE_ROLE_NON_REMOVABLE_LAST_ROLE.value.format(
                    employee_role=role_to_remove.name,
                    employee_id=employee_to_remove_role.id,
                    role_count=total_employee_to_remove_roles,
                )
                self._log.debug(err_msg)
                raise EmployeeNonRemovableEmployeeRoleError(status_code=status.HTTP_403_FORBIDDEN, detail=err_msg)
            charity_employee_to_remove_role = await self.charity_employee_service.get_charity_employee_by_charity_and_employee_id( # noqa
                charity_id,
                employee_id,
            )
            # Removing role from charity_employee.
            await self.employee_role_db_service.remove_employee_role_from_charity_employee(
                charity_employee_to_remove_role,
                role_to_remove,
            )
            #
            EmployeeRoleServiceConstants.SUCCESSFUL_EMPLOYEE_ROLE_REMOVAL_MSG.value['message'] = (
                EmployeeRoleServiceConstants.SUCCESSFUL_EMPLOYEE_ROLE_REMOVAL_MSG.value['message'].format(
                    role_id=role_to_remove.id,
                    employee_id=employee_to_remove_role.id,
                )
            )
            return EmployeeRoleServiceConstants.SUCCESSFUL_EMPLOYEE_ROLE_REMOVAL_MSG.value
