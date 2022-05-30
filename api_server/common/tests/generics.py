from datetime import timedelta
from unittest.mock import AsyncMock
from uuid import uuid4
import os
import random

from fastapi import FastAPI

from alembic.config import Config
from asgi_lifespan import LifespanManager
from celery import Celery
from databases import Database
from fastapi_jwt_auth import AuthJWT
from httpx import AsyncClient
from pytest import fixture
from pytest_mock.plugin import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import alembic
import pytest_asyncio

from app import create_app
from app.celery_base import create_celery_app
from auth.cruds import ChangePasswordTokenCRUD, EmailConfirmationTokenCRUD
from auth.models import ChangePasswordToken, EmailConfirmationToken
from auth.services import AuthService
from auth.utils.jwt_tokens import create_jwt_token, create_token_payload
from charity.models import CharityOrganisation, CharityUserAssociation
from common.constants.api import ApiConstants
from common.constants.auth import AuthJWTConstants, ChangePasswordTokenConstants, EmailConfirmationTokenConstants
from common.constants.celery import CeleryConstants
from common.constants.tests import GenericTestConstants
from common.tests.test_data.charity.charity_requests import initialize_charity_data
from common.tests.test_data.users import (
    request_test_user_data,
    request_test_user_pictures_data,
    user_pictures_mock_data,
)
from db import create_engine
from users.cruds import UserCRUD, UserPictureCRUD
from users.models import User, UserPicture
from users.schemas import UserInputSchema
from users.utils.aws_s3 import S3Client
from users.utils.aws_s3.user_pictures import UserImageFile
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
    async def user_crud(self, db_session: AsyncSession) -> UserCRUD:
        """A pytest fixture that creates instance of user_crud business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of UserCRUD business logic class.
        """
        return UserCRUD(session=db_session)

    async def _create_user(self, user_crud: UserCRUD, user: UserInputSchema) -> User:
        """Stores user test data in test database.

        Args:
            user_crud: instance of business logic class.
            user: serialized UserInputSchema object.

        Returns:
        newly created User object.
        """
        return await user_crud.add_user(user)

    @pytest_asyncio.fixture
    async def test_user(self, user_crud: UserCRUD) -> User:
        """Create test user data and store it in test database.

        Args:
            user_crud: instance of business logic class.

        Returns:
        newly created User object.
        """
        return await self._create_user(user_crud, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))

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
                    follow_redirects=True,
            ) as client:
                yield client

    @pytest_asyncio.fixture(autouse=True)
    async def auth_service(self, db_session: AsyncSession, user_crud: fixture) -> AuthService:
        """A pytest fixture that creates instance of auth_service business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.
            user_crud: instance of business logic class.

        Returns:
        An instance of AuthService business logic class.
        """
        return AuthService(session=db_session, Authorize=AuthJWT())

    @pytest_asyncio.fixture
    async def authenticated_test_user(
            self, client: fixture, user_crud: UserCRUD, auth_service: AuthService,
    ) -> User:
        """Create authenticated test user data and store it in test database.

        Args:
            user_crud: instance of user business logic class.
            auth_service: instance of auth business logic class.

        Returns:
        newly created User object.
        """
        user = await self._create_user(user_crud, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
        return await self._create_authenticated_user(user, auth_service, client)

    async def _create_authenticated_user(self, user: User, auth_service: AuthService, client: fixture) -> User:
        """Modifies 'client' fixture by adding JWT cookies for user authentication.

        Args:
            user_crud: instance of business logic class.
            user: User instance.
            client: pytest fixture that creates test httpx client.

        Returns:
        newly created User object.
        """
        user_claims = {
            'user_data': {
                'id': str(user.id),
                'email': user.email,
                'phone': user.phone_number,
            },
        }
        access_token = await auth_service._create_jwt_token(
            subject=user.username,
            token_type=AuthJWTConstants.ACCESS_TOKEN_NAME.value,
            time_unit=AuthJWTConstants.MINUTES.value,
            time_amount=AuthJWTConstants.TOKEN_EXPIRE_60.value,
            user_claims=user_claims,
        )
        refresh_token = await auth_service._create_jwt_token(
            subject=user.username,
            token_type=AuthJWTConstants.REFRESH_TOKEN_NAME.value,
            time_unit=AuthJWTConstants.DAYS.value,
            time_amount=AuthJWTConstants.TOKEN_EXPIRE_7.value,
            user_claims=user_claims,
        )
        client.cookies.update({AuthJWTConstants.ACCESS_TOKEN_COOKIE_NAME.value: access_token})
        client.cookies.update({AuthJWTConstants.REFRESH_TOKEN_COOKIE_NAME.value: refresh_token})
        return user

    @pytest_asyncio.fixture
    async def random_test_user(self, user_crud: UserCRUD) -> User:
        """Create test User object with random data and store it in test database.

        Args:
            user_crud: instance of business logic class.

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
        return await self._create_user(user_crud, UserInputSchema(**ADD_RANDOM_USER_TEST_DATA))

    @pytest_asyncio.fixture(autouse=True)
    async def user_picture_crud(self, db_session: AsyncSession) -> UserPictureCRUD:
        """A pytest fixture that creates instance of user_picture_crud database logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of UserPictureCRUD database logic class.
        """
        return UserPictureCRUD(session=db_session)

    @pytest_asyncio.fixture
    async def test_user_picture(self, user_crud: UserCRUD, user_picture_crud: UserPictureCRUD) -> UserPicture:
        """Creates test UserPicture object and storing it in the test databases.

        Args:
            user_picture_crud: instance of database crud logic class.

        Returns:
        newly created UserPicture object.
        """
        user = await self._create_user(user_crud, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
        return await user_picture_crud.add_user_picture(user.id)

    @pytest_asyncio.fixture
    async def authenticated_test_user_picture(
            self, user_crud: UserCRUD, user_picture_crud: UserPictureCRUD, auth_service: AuthService, client: fixture,
    ) -> UserPicture:
        """Creates test UserPicture object and storing it in the test databases.

        Args:
            user_picture_crud: instance of database crud logic class.

        Returns:
        newly created UserPicture object.
        """
        user = await self._create_user(user_crud, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
        await self._create_authenticated_user(user, auth_service, client)
        return await user_picture_crud.add_user_picture(user.id)

    @pytest_asyncio.fixture(autouse=True)
    async def celery_app(self):
        """Create Celery app instance to use it in tests.

        Returns:
        an instance of FastAPI.
        """
        return create_celery_app(config_name=CeleryConstants.TESTING_CONFIG.value)

    @pytest_asyncio.fixture
    async def test_S3Client(self, celery_app: Celery) -> S3Client:
        """A pytest fixture that creates instance of S3Client.

        Args:
            celery_app: pytest fixture that creates test Celery app.

        Returns:
        An instance of S3Client.
        """
        return S3Client(
            aws_access_key_id=celery_app.conf.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=celery_app.conf.get('AWS_SECRET_ACCESS_KEY'),
            aws_s3_bucket_region=celery_app.conf.get('AWS_S3_BUCKET_REGION'),
            aws_s3_bucket_name=celery_app.conf.get('AWS_S3_BUCKET_NAME'),
        )

    @pytest_asyncio.fixture
    async def test_user_image_file(self, test_user_picture: UserPicture) -> UserImageFile:
        """A pytest fixture that creates instance of UserImageFile.

        Args:
            test_user_picture: instance of UserPicture object.

        Returns:
        An instance of UserImageFile object.
        """
        return UserImageFile(
            db_user_picture=test_user_picture,
            image_data=request_test_user_pictures_data.TEST_USER_PICTURE_VALID_JPEG.read(),
            content_type=request_test_user_pictures_data.TEST_USER_PICTURE_CONTENT_TYPE,
            file_extension=request_test_user_pictures_data.TEST_USER_PICTURE_EXTENSION,
        )

    @pytest_asyncio.fixture
    async def mock_upload_file_object(self, mocker: MockerFixture) -> AsyncMock:
        """A pytest fixture creates mocked return value for 'S3Client.upload_file_object()' method.

        Args:
            mocker: A pytest_mock lib fixture.

        Returns:
        An instance of AsyncMock object with mocked return value for 'S3Client.upload_file_object()' method.
        """
        async_mock = AsyncMock()
        mocker.patch('users.utils.aws_s3.S3Client.upload_file_object', side_effect=async_mock)
        async_mock.return_value = user_pictures_mock_data.S3Client_upload_image_to_s3_valid_response
        return async_mock

    @pytest_asyncio.fixture
    async def mock_delete_file_objects(self, mocker: MockerFixture) -> AsyncMock:
        """A pytest fixture creates mocked return value for 'S3Client.delete_file_objects()' method.

        Args:
            mocker: A pytest_mock lib fixture.

        Returns:
        An instance of AsyncMock object with mocked return value for 'S3Client.delete_file_objects()' method.
        """
        async_mock = AsyncMock()
        mocker.patch('users.utils.aws_s3.S3Client.delete_file_objects', side_effect=async_mock)
        async_mock.return_value = user_pictures_mock_data.S3Client_delete_images_in_s3_valid_response
        return async_mock

    @staticmethod
    async def _initialize_charity(user: User, db_session: AsyncSession, charity_title: str) -> CharityOrganisation:
        """
        Initializes charityOrganisation in database.
        Args:
                user: instance of User business logic class.
                db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
            newly created CharityOrganisation object.
        """
        organisation = CharityOrganisation(**initialize_charity_data(charity_title))
        association = CharityUserAssociation()
        association.user = user
        organisation.users_association.append(association)

        db_session.add(organisation)
        await db_session.commit()
        await db_session.refresh(organisation)
        return organisation

    @pytest_asyncio.fixture
    async def charity(self, user_crud: UserCRUD, db_session: AsyncSession) -> CharityOrganisation:
        """
            Create authenticated test charity data and store it in test database.

            Returns:
            CharityOrganisation object and not authenticated User object.
            """

        user = await self._create_user(user_crud, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
        organisation = await self._initialize_charity(
            user=user,
            db_session=db_session,
            charity_title="Charity Organisation"
        )
        return organisation

    @pytest_asyncio.fixture
    async def authenticated_user_charity(self,
                                         user_crud: UserCRUD,
                                         db_session: AsyncSession,
                                         auth_service: AuthService,
                                         client: fixture, ) -> CharityOrganisation:
        """
        Create authenticated test charity data and store it in test database.

            Returns:
        CharityOrganisation object.
        """
        user = await self._create_user(user_crud, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
        organisation = await self._initialize_charity(user=user, db_session=db_session,
                                                      charity_title="Charity Organisation")
        await self._create_authenticated_user(user, auth_service, client)

        return organisation

    @pytest_asyncio.fixture
    async def authenticated_random_test_user(self, random_test_user: User,
                                             auth_service: AuthService,
                                             client: fixture):
        return await self._create_authenticated_user(random_test_user, auth_service, client)

    @pytest_asyncio.fixture
    async def many_charities(self, user_crud: UserCRUD, db_session: AsyncSession):
        user = await self._create_user(user_crud, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
        charity_titles = ("organisation D", "organisation B", "organisation A", "organisation Y")
        organisations = [await self._initialize_charity(user=user, db_session=db_session, charity_title=title)
                         for title in charity_titles]
        return organisations

    @pytest_asyncio.fixture(autouse=True)
    async def email_confirmation_token_crud(self, db_session: AsyncSession) -> EmailConfirmationTokenCRUD:
        """A pytest fixture that creates instance of email_confirmation_token_crud business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of EmailConfirmationTokenCRUD business logic class.
        """
        return EmailConfirmationTokenCRUD(session=db_session)

    @pytest_asyncio.fixture
    async def test_email_confirmation_token(
            self, email_confirmation_token_crud: EmailConfirmationTokenCRUD, user_crud: UserCRUD,
            db_session: AsyncSession,
    ) -> EmailConfirmationToken:
        """A pytest fixture that creates test EmailConfirmationToken object and storing it in the test databases.

        Args:
            email_confirmation_token_crud: instance of database crud logic class.
            user_crud: instance of database crud logic class.
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of EmailConfirmationToken object.
        """
        user = await self._create_user(user_crud, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
        jwt_token_payload = create_token_payload(
            data=str(user.id),
            time_amount=EmailConfirmationTokenConstants.TOKEN_EXPIRE_7.value,
            time_unit=EmailConfirmationTokenConstants.MINUTES.value,
        )
        jwt_token = create_jwt_token(payload=jwt_token_payload, key=user.password)
        db_token = await email_confirmation_token_crud.add_email_confirmation_token(id_=user.id, token=jwt_token)
        db_token.created_at = db_token.created_at - timedelta(**EmailConfirmationTokenConstants.TIMEDELTA_10_MIN.value)
        db_session.add(db_token)
        await db_session.commit()
        await db_session.refresh(db_token)
        return db_token

    @pytest_asyncio.fixture
    async def test_activated_email_confirmation_token(
            self,
            test_email_confirmation_token: EmailConfirmationToken,
            email_confirmation_token_crud: EmailConfirmationTokenCRUD,
            db_session: AsyncSession,
    ) -> EmailConfirmationToken:
        """A pytest fixture that creates activated test User object and storing it in the test databases.

        Args:
            test_email_confirmation_token: pytest fixture that creates test EmailConfirmationToken object.
            email_confirmation_token_crud: instance of database crud logic class.
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        A User object with filled 'activated_at' field.
        """
        await email_confirmation_token_crud._activate_user_by_id(test_email_confirmation_token.user.id)
        await email_confirmation_token_crud._expire_email_confirmation_token_by_id(test_email_confirmation_token.id)
        await db_session.refresh(test_email_confirmation_token)
        return test_email_confirmation_token

    @pytest_asyncio.fixture(autouse=True)
    async def change_password_token_crud(self, db_session: AsyncSession) -> ChangePasswordTokenCRUD:
        """A pytest fixture that creates instance of change_password_token_crud business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of ChangePasswordTokenCRUD business logic class.
        """
        return ChangePasswordTokenCRUD(session=db_session)

    @pytest_asyncio.fixture
    async def test_change_password_token(
            self, change_password_token_crud: ChangePasswordTokenCRUD, user_crud: UserCRUD,
            db_session: AsyncSession,
    ) -> ChangePasswordToken:
        """A pytest fixture that creates test ChangePasswordToken object and storing it in the test databases.

        Args:
            change_password_token_crud: instance of database crud logic class.
            user_crud: instance of database crud logic class.
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of EmailConfirmationToken object.
        """
        user = await self._create_user(user_crud, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
        jwt_token_payload = create_token_payload(
            data=str(user.id),
            time_amount=ChangePasswordTokenConstants.TOKEN_EXPIRE_1.value,
            time_unit=ChangePasswordTokenConstants.DAYS.value,
        )
        jwt_token = create_jwt_token(payload=jwt_token_payload, key=user.password)
        db_token = await change_password_token_crud.add_change_password_token(id_=user.id, token=jwt_token)
        db_token.created_at = db_token.created_at - timedelta(**ChangePasswordTokenConstants.TIMEDELTA_10_MIN.value)
        db_session.add(db_token)
        await db_session.commit()
        await db_session.refresh(db_token)
        return db_token
