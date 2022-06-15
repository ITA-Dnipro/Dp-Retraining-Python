from pydantic import BaseModel

from common.constants.prepopulates.fundraise_statuses import FundraiseStatusPopulateData
from db import create_engine
from fundraisers.dao import FundraiseStatusDAO
from fundraisers.schemas import FundraiseStatusInputSchema
from utils.orm_helpers import create_db_session


async def populate_fundraise_statuses_table(config: BaseModel) -> None:
    """Populates app db FundraiseStatus table with data.

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
        for status in FundraiseStatusPopulateData.ALL_STATUSES.value:
            fundraise_status_dao = FundraiseStatusDAO(session)
            db_fundraise_status = await fundraise_status_dao.get_fundraise_status_by_name(name=status)
            if not db_fundraise_status:
                fundraise_status = FundraiseStatusInputSchema(name=status)
                await fundraise_status_dao.add_fundraise_status(fundraise_status)
