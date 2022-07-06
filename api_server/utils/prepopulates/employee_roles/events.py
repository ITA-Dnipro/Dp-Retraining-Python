from pydantic import BaseModel

from charities.db_services import EmployeeRoleDBService
from charities.schemas import EmployeeRoleInputSchema
from common.constants.prepopulates import EmployeeRolePopulateData
from db import create_engine
from utils.orm_helpers import create_db_session


async def populate_employee_roles_table(config: BaseModel) -> None:
    """Populates app db EmployeeRole table with data.

    Args:
        config: fastapi app config.

    Returns:
    Nothing.
    """
    engine = create_engine(
        database_url=config.POSTGRES_DATABASE_URL,
        echo=config.API_SQLALCHEMY_ECHO,
        future=config.API_SQLALCHEMY_FUTURE,
    )
    db_session = create_db_session(engine)
    async with db_session as session:
        for role in EmployeeRolePopulateData.ALL_ROLES.value:
            employee_role_db_service = EmployeeRoleDBService(session)
            db_employee_role = await employee_role_db_service.get_employee_role_by_name(name=role)
            if not db_employee_role:
                employee_role = EmployeeRoleInputSchema(name=role)
                await employee_role_db_service.add_employee_role(employee_role)
