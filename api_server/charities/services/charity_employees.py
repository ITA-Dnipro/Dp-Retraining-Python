from uuid import UUID

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from charities.db_services import CharityEmployeeDBService
from charities.models import Charity
from charities.schemas import EmployeeInputSchema
from charities.services.commons import CharityCommonService
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

    async def add_employee_to_charity(
            self, charity_id: UUID, employee_data: EmployeeInputSchema,
    ) -> Charity:
        """Add User to Charity object in the database via many-to-many relationship.

        Args:
            charity_id: UUID of charity.
            employee_data: Serialized EmployeeInputSchema object.

        Returns:
        Charity object with User added to many-to-many relationship.
        """
        return await self._add_employee_to_charity(charity_id, employee_data)

    async def _add_employee_to_charity(
            self, charity_id: UUID, employee_data: EmployeeInputSchema,
    ) -> Charity:
        user = await self.user_service.get_user_by_id(employee_data.user_id)
        charity = await self.get_charity_by_id(charity_id)
        await self.save_employee_to_charity(user, charity)
        return user
