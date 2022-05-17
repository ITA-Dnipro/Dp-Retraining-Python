from uuid import uuid4
import os
import random

from fastapi import FastAPI

from alembic.config import Config
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi_jwt_auth import AuthJWT
from httpx import AsyncClient
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import alembic
import pytest_asyncio

from app import create_app
from auth.services import AuthService
from balances.models import Balance
from balances.schemas import BalanceInputSchema
from balances.services import BalanceService
from common.constants.api import ApiConstants
from common.constants.auth import AuthJWTConstants
from common.constants.tests import GenericTestConstants
from common.tests.test_data.users import request_test_user_data
from db import create_engine
from donations.models import Donation
from donations.schemas import DonationInputSchema
from donations.services import DonationService
from refills.models import Refill
from refills.schemas import RefillInputSchema
from refills.services import RefillService
from users.models import User
from users.schemas import UserInputSchema
from users.services import UserService
from utils.tests import find_fullpath


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
    def make_alembic_migrations(self, setup_db: fixture, app: FastAPI) -> None:
        """A pytest fixture to run alembic migrations after creation of test database.

        Args:
            setup_db: pytest fixture that creates test database.
            app: pytest fixture that creates test FastAPI instance.

        Returns:
        Nothing.
        """
        alembic_ini_filepath = find_fullpath(
            GenericTestConstants.ALEMBIC_INI_FILENAME.value,
            GenericTestConstants.ROOT_FILEPATH.value,
        )
        config = Config(alembic_ini_filepath)
        alembic_migrations_filepath = ''.join(
            [
                os.path.dirname(alembic_ini_filepath),
                GenericTestConstants.ALEMBIC_MIGRATIONS_FOLDER.value,
            ]
        )
        config.set_main_option(GenericTestConstants.SQLALCHEMY_URL_OPTION.value, app.app_config.POSTGRES_DATABASE_URL)
        config.set_main_option(GenericTestConstants.SCRIPT_LOCATION_OPTION.value, alembic_migrations_filepath)
        alembic.command.upgrade(config, GenericTestConstants.ALEMBIC_HEAD.value)

    @pytest_asyncio.fixture(autouse=True)
    async def user_service(self, db_session: AsyncSession) -> UserService:
        """A pytest fixture that creates instance of user_service business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of UserService business logic class.
        """
        return UserService(session=db_session, Authorize=AuthJWT())

    async def _create_user(self, user_service: UserService, user: UserInputSchema) -> User:
        """Stores user test data in test database.

        Args:
            user_service: instance of business logic class.
            user: serialized UserInputSchema object.

        Returns:
        newly created User object.
        """
        return await user_service.add_user(user)

    @pytest_asyncio.fixture
    async def test_user(self, user_service: UserService) -> User:
        """Create test user data and store it in test database.

        Args:
            user_service: instance of business logic class.

        Returns:
        newly created User object.
        """
        return await self._create_user(user_service, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))

    @pytest_asyncio.fixture(autouse=True)
    async def client(self, app: FastAPI) -> AsyncClient:
        """A pytest fixture that creates AsyncClient instance.

        Args:
            app: pytest fixture that creates test FastAPI instance.

        Returns:
        An instance of AsyncClient.
        """
        async with LifespanManager(app):
            async with AsyncClient(
                    app=app,
                    base_url=GenericTestConstants.BASE_URL_TEMPLATE.value.format(
                        api_host=app.app_config.API_SERVER_HOST,
                        api_port=app.app_config.API_SERVER_PORT,
                    ),
                    headers=GenericTestConstants.TEST_CLIENT_HEADERS.value,
                    follow_redirects=True,
            ) as client:
                yield client

    @pytest_asyncio.fixture(autouse=True)
    async def auth_service(self, db_session: AsyncSession, user_service: fixture) -> UserService:
        """A pytest fixture that creates instance of auth_service business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.
            user_service: instance of business logic class.

        Returns:
        An instance of AuthService business logic class.
        """
        return AuthService(session=db_session, Authorize=AuthJWT(), user_service=user_service)

    @pytest_asyncio.fixture
    async def authenticated_test_user(
            self, client: fixture, user_service: UserService, auth_service: AuthService,
    ) -> User:
        """Create authenticated test user data and store it in test database.

        Args:
            user_service: instance of user business logic class.
            auth_service: instance of auth business logic class.

        Returns:
        newly created User object.
        """
        user = await self._create_user(user_service, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
        return await self._create_authenticated_user(user, auth_service, client)

    async def _create_authenticated_user(self, user: User, auth_service: AuthService, client: fixture) -> User:
        """Modifies 'client' fixture by adding JWT cookies for user authentication.

        Args:
            user_service: instance of business logic class.
            user: User instance.
            client: pytest fixture that creates test httpx client.

        Returns:
        newly created User object.
        """
        access_token = await auth_service._create_jwt_token(
            subject=user.username,
            token_type=AuthJWTConstants.ACCESS_TOKEN_NAME.value,
            time_unit=AuthJWTConstants.MINUTES.value,
            time_amount=AuthJWTConstants.TOKEN_EXPIRE_60.value,
        )
        refresh_token = await auth_service._create_jwt_token(
            subject=user.username,
            token_type=AuthJWTConstants.REFRESH_TOKEN_NAME.value,
            time_unit=AuthJWTConstants.DAYS.value,
            time_amount=AuthJWTConstants.TOKEN_EXPIRE_7.value,

        )
        client.cookies.update({AuthJWTConstants.ACCESS_TOKEN_COOKIE_NAME.value: access_token})
        client.cookies.update({AuthJWTConstants.REFRESH_TOKEN_COOKIE_NAME.value: refresh_token})
        return user

    @pytest_asyncio.fixture
    async def random_test_user(self, user_service: UserService) -> User:
        """Create test User object with random data and store it in test database.

        Args:
            user_service: instance of business logic class.

        Returns:
        newly created User object with random data.
        """
        ADD_RANDOM_USER_TEST_DATA = {
            'username': f'test_john_{uuid4()}',
            'first_name': 'john',
            'last_name': 'bar',
            'email': f'test_john{random.randrange(1000000000, 9999999999)}@john.com',
            'password': '12345678',
            'phone_number': f'+38{random.randrange(1000000000, 9999999999)}',
        }
        return await self._create_user(user_service, UserInputSchema(**ADD_RANDOM_USER_TEST_DATA))

    @pytest_asyncio.fixture(autouse=True)
    async def balance_service(self, db_session: AsyncSession) -> BalanceService:
        """A pytest fixture that creates instance of balance_service business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of UserService business logic class.
        """
        return BalanceService(session=db_session, Authorize=AuthJWT())

    async def _create_balance(self, balance_service: BalanceService, balance: BalanceInputSchema) -> Balance:
        """Stores user test data in test database.

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
        test_balance = {'amount': 0}
        return await self._create_balance(balance_service,
                                          BalanceInputSchema(**test_balance))

    @pytest_asyncio.fixture(autouse=True)
    async def donation_service(self, db_session: AsyncSession) -> DonationService:
        """A pytest fixture that creates instance of donation_service business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of UserService business logic class.
        """
        return DonationService(session=db_session, Authorize=AuthJWT())

    async def _create_donation(self, donation_service: DonationService, donation: DonationInputSchema) -> Donation:
        """Stores user test data in test database.

        Args:
            donation_service: instance of business logic class.
            donation: serialized DonationInputSchema object.

        Returns:
        newly created donation object.
        """
        return await donation_service._add_donation(donation)

    @pytest_asyncio.fixture
    async def test_donation(self, donation_service: DonationService, authenticated_test_user: User,
                            user_service: UserService) -> Donation:
        """Create test donation data and store it in test database.

        Args:
            donation_service: instance of business logic class.

        Returns:
        newly created Balance object.
        """
        recipient_user_data = {
            'password': '12345678',
            'username': 'updated_test_john',
            'first_name': 'updated_john',
            'last_name': 'updated_bar',
            'email': 'updated_john@john.com',
            'phone_number': '+380994445566',
        }
        donation_test_data = {
            'amount': 1,
            "sender_id": authenticated_test_user.balance_id,
            "recipient_id": (await self._create_user(user_service, UserInputSchema(
                **recipient_user_data))).balance_id,
        }
        return await self._create_donation(donation_service,
                                           DonationInputSchema(**donation_test_data))

    @pytest_asyncio.fixture(autouse=True)
    async def refill_service(self, db_session: AsyncSession) -> RefillService:
        """A pytest fixture that creates instance of refill_service business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of UserService business logic class.
        """
        return RefillService(session=db_session, Authorize=AuthJWT())

    async def _create_refill(self, refill_service: RefillService, refill: RefillInputSchema) -> Refill:
        """Stores user test data in test database.

        Args:
            refill_service: instance of business logic class.
            refill: serialized RefillInputSchema object.

        Returns:
        newly created refill object.
        """
        return await refill_service._add_refill(refill)

    @pytest_asyncio.fixture
    async def test_refill(self, refill_service: RefillService,
                          authenticated_test_user: User) -> Refill:
        """Create test refill data and store it in test database.

        Args:
            refill_service: instance of business logic class.

        Returns:
        newly created Balance object.
        """
        refill_test_data = {
            'amount': 1,
            "balance_id": authenticated_test_user.balance_id,
        }
        return await self._create_refill(refill_service,
                                         RefillInputSchema(**refill_test_data))
