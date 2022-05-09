from fastapi import FastAPI

from databases import Database
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from users.models import Balance
from users.schemas import BalanceInputSchema
from users.services import BalanceService
import pytest_asyncio

from app import create_app
from common.constants.api import ApiConstants
from common.constants.tests import GenericTestConstants
from db import create_engine


class TestMixin:
    """Generic test helper class."""

    @pytest_asyncio.fixture(autouse=True)
    async def db_session(self, make_alembic_migrations: fixture, app: FastAPI) -> AsyncSession:
        """A pytest fixture to create sqlalchemy AsyncSession instance to use in tests.

        Args:
            make_alembic_migrations: pytest fixture that runs alembic migrations.
            app: pytest fixture that creates test FastAPI instance.

        Returns:

        """
        engine = create_engine(
            database_url=app.app_config.POSTGRES_DATABASE_URL,
            echo=app.app_config.API_SQLALCHEMY_ECHO,
            future=app.app_config.API_SQLALCHEMY_FUTURE,
        )
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False,
        )
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.close()
                await engine.dispose()

    async def _database_exists(self, db_connect: Database, db_query: str) -> int | None:
        """Query postgres server and get database id.

        Args:
            db_connect: Database connect instance.
            db_query: string with sql query.

        Returns:
        int id of database in postgres server or None.
        """
        async with db_connect as connection:
            return await connection.execute(db_query)

    async def database_exists(self, db_connect: Database, db_query: str) -> bool:
        """Checks if database exists in postgres server.

        Args:
            db_connect: Database connect instance.
            db_query: string with sql query.

        Returns:
        bool of presence database in postgres server.
        """
        return bool(await self._database_exists(db_connect, db_query))

    async def _delete_database(self, db_connect: Database, db_query: str) -> None:
        """Executes sql query to delete database in postgres server.

        Args:
            db_connect: Database connect instance.
            db_query: string with sql query.

        Returns:
        Nothing.
        """
        async with db_connect as connection:
            await connection.execute(db_query)

    async def delete_database(self, db_connect: Database, db_name: str) -> None:
        """Delete test database in postgres server.

        Args:
            db_connect: Database connect instance.
            db_name: name of postgres database.

        Returns:
        Nothing.
        """
        db_query = GenericTestConstants.DELETE_DATABASE_QUERY.value.format(db_name=db_name)
        await self._delete_database(db_connect, db_query)

    async def _create_database(self, db_connect: Database, db_query: str) -> None:
        """Executes sql query to create database in postgres server.

        Args:
            db_connect: Database connect instance.
            db_query: string with sql query.

        Returns:
        Nothing.
        """
        async with db_connect as connection:
            await connection.execute(db_query)

    @pytest_asyncio.fixture(autouse=True)
    def app(self) -> FastAPI:
        """Create FastAPI instance to use it in tests.

        Returns:
        an instance of FastAPI.
        """
        return create_app(config_name=ApiConstants.TESTING_CONFIG.value)

    async def create_database(self, default_db: Database, db_name: str) -> None:
        """Creates test database in postgres server.

        Args:
            default_db: Database connect instance.
            db_name: name of postgres database.

        Returns:
        Nothing.
        """
        if await self.database_exists(
                db_connect=default_db,
                db_query=GenericTestConstants.SELECT_DATABASE_QUERY.value.format(
                    db_name=db_name,
                ),
        ):
            await self.delete_database(
                db_connect=default_db,
                db_name=db_name,
            )
        await self._create_database(
            db_connect=default_db,
            db_query=GenericTestConstants.CREATE_DATABASE_QUERY.value.format(
                db_name=db_name,
            ),
        )

    @pytest_asyncio.fixture(autouse=True)
    async def setup_db(self, app: FastAPI) -> None:
        """Creates test database before test run, and delete it afterwards.

        Args:
            app: pytest fixture that creates test FastAPI instance.

        Returns:
        Nothing
        """
        default_db = Database(app.app_config.DEFAULT_POSTGRES_DATABASE_URL)
        await self.create_database(default_db, db_name=app.app_config.POSTGRES_DB_NAME)
        yield
        await self.delete_database(default_db, db_name=app.app_config.POSTGRES_DB_NAME)

    @pytest_asyncio.fixture(autouse=True)
    async def balance_service(self, db_session: AsyncSession) -> BalanceService:
        """A pytest fixture that creates instance of balance_service business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of BalanceService business logic class.
        """
        return BalanceService(session=db_session)

    async def _create_balance(self, balance_service: BalanceService, balance: BalanceInputSchema) -> Balance:
        """Stores balance test data in test database.

        Args:
            balance_service: instance of business logic class.
            balance: serialized BalanceInputSchema object.

        Returns:
        newly created Balance object.
        """
        return await balance_service.add_balance(balance)

    @pytest_asyncio.fixture
    async def test_balance(self, balance_service: BalanceService) -> Balance:
        """Create test balance data and store it in test database.

        Args:
            balance_service: instance of business logic class.

        Returns:
        newly created Balance object.
        """
        test_balance = {'amount': 10}
        return await self._create_balance(balance_service, BalanceInputSchema(**test_balance))
