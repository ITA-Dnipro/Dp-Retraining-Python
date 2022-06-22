from uuid import UUID

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from charities.db_services import CharityEmployeeDBService, EmployeeDBService, EmployeeRoleDBService
from charities.models import Charity, CharityEmployeeAssociation
from charities.schemas import EmployeeDBSchema, EmployeeInputSchema
from charities.services.commons import CharityCommonService
from charities.utils.jwt import jwt_charity_validator
from charities.utils.role_permissions import employee_role_validator, get_allowed_roles_for_employee_role
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
    ) -> CharityEmployeeAssociation:
        """Add User to Charity object in the database via many-to-many relationship.

        Args:
            charity_id: UUID of charity.
            jwt_subject: decoded jwt identity.
            employee_data: Serialized EmployeeInputSchema object.

        Returns:
        Charity object with User added to many-to-many relationship.
        """
        return await self._add_employee_to_charity(charity_id, jwt_subject, employee_data)

    async def _add_employee_to_charity(
            self, charity_id: UUID, jwt_subject: str, employee_data: EmployeeInputSchema,
    ) -> CharityEmployeeAssociation:
        # Getting list of allowed roles for new eployee role.
        allowed_roles = get_allowed_roles_for_employee_role(role_name=employee_data.role)
        # Checking if currently authenticated user is in Charity employees list.
        db_charity = await self.get_charity_by_id_with_relationships(charity_id)
        db_charity_employee_usernames = [employee.user.username for employee in db_charity.employees]
        if jwt_charity_validator(jwt_subject=jwt_subject, usernames=db_charity_employee_usernames):
            # Checking if currently authenticated employee have sufficient roles to add employee with role.
            for current_db_employee in db_charity.employees:
                if current_db_employee.user.username == jwt_subject:
                    break
            current_db_employee_roles = [role for role in current_db_employee.roles]
            current_db_employee_role_names = [role.name for role in current_db_employee_roles]
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
                # Refreshing charity and returning newly added employee with roles.
                await self.charity_db_service.refresh_charity(db_charity)
                return new_db_employee
