from contextlib import contextmanager
from datetime import datetime, timedelta
from unittest.mock import AsyncMock
from uuid import uuid4
import os
import random
import time

from fastapi import FastAPI

from alembic.config import Config
from asgi_lifespan import LifespanManager
from celery import Celery
from databases import Database
from fastapi_jwt_auth import AuthJWT
from freezegun import freeze_time
from httpx import AsyncClient
from pytest import fixture
from pytest_mock.plugin import MockerFixture
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import alembic
import pytest
import pytest_asyncio

from app import create_app
from app.celery_base import create_celery_app
from auth.cruds import ChangePasswordTokenCRUD, EmailConfirmationTokenCRUD
from auth.models import ChangePasswordToken, EmailConfirmationToken
from auth.services import AuthService
from auth.utils.jwt_tokens import create_jwt_token, create_token_payload
from charities.models import Charity
from charities.schemas import CharityInputSchema
from charities.services import CharityService
from common.constants.api import ApiConstants
from common.constants.auth import AuthJWTConstants, ChangePasswordTokenConstants, EmailConfirmationTokenConstants
from common.constants.celery import CeleryConstants
from common.constants.tests import GenericTestConstants
from common.tests.test_data.auth import request_test_auth_email_confirmation_data
from common.tests.test_data.charities import request_test_charity_data
from common.tests.test_data.users import (
    request_test_user_data,
    request_test_user_pictures_data,
    user_pictures_mock_data,
)
from db import create_engine
from users.cruds import UserPictureCRUD
from users.models import User, UserPicture
from users.schemas import UserInputSchema
from users.services import UserService
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
    async def user_service(self, db_session: AsyncSession) -> UserService:
        """A pytest fixture that creates instance of user_service business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of UserService business logic class.
        """
        return UserService(session=db_session)

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
    async def test_user(self, user_service: UserService, patch_model_current_time: fixture, request: fixture) -> User:
        """Create test user data and store it in test database.

        Args:
            user_service: instance of business logic class.
            patch_model_current_time: pytest fixture that alters datetime that saves in db model.
            request: native pytest fixture.

        Returns:
        newly created User object.
        """
        if not hasattr(request, 'param'):
            return await self._create_user(user_service, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
        with patch_model_current_time(**request.param):
            return await self._create_user(
                user_service,
                UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA),
            )

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
    async def auth_service(self, db_session: AsyncSession) -> AuthService:
        """A pytest fixture that creates instance of auth_service business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of AuthService business logic class.
        """
        return AuthService(session=db_session)

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
            user_crud: instance of business logic class.
            user: User instance.
            client: pytest fixture that creates test httpx client.

        Returns:
        newly created User object.
        """
        Authorize = AuthJWT()
        user_claims = {
            'user_data': {'id': str(user.id)},
        }
        access_token = Authorize.create_access_token(
            subject=user.username,
            expires_time=timedelta(**AuthJWTConstants.TOKEN_LIFETIME_60_MINUTES.value),
            user_claims=user_claims,
            fresh=True,
        )
        refresh_token = Authorize.create_refresh_token(
            subject=user.username,
            expires_time=timedelta(**AuthJWTConstants.TOKEN_LIFETIME_7_DAYS.value),
            user_claims=user_claims,
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
    async def user_picture_crud(self, db_session: AsyncSession) -> UserPictureCRUD:
        """A pytest fixture that creates instance of user_picture_crud database logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of UserPictureCRUD database logic class.
        """
        return UserPictureCRUD(session=db_session)

    @pytest_asyncio.fixture
    async def test_user_picture(self, user_service: UserService, user_picture_crud: UserPictureCRUD) -> UserPicture:
        """Creates test UserPicture object and storing it in the test databases.

        Args:
            user_service: instance of business logic class.
            user_picture_crud: instance of database crud logic class.

        Returns:
        newly created UserPicture object.
        """
        user = await self._create_user(user_service, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
        return await user_picture_crud.add_user_picture(user.id)

    @pytest_asyncio.fixture
    async def authenticated_test_user_picture(
            self, user_service: UserService, user_picture_crud: UserPictureCRUD, auth_service: AuthService,
            client: fixture,
    ) -> UserPicture:
        """Creates test UserPicture object and storing it in the test databases.

        Args:
            user_service: instance of business logic class.
            user_picture_crud: instance of database crud logic class.
            auth_service: instance of business logic class.
            client: pytest fixture that creates test httpx client.

        Returns:
        newly created UserPicture object.
        """
        user = await self._create_user(user_service, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
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
    @pytest.mark.parametrize(
        'test_user',
        [request_test_auth_email_confirmation_data.EMAIL_CONFIRMATION_TOKEN_MOCK_CREATED_AT_DATA],
        indirect=['test_user'],
    )
    async def test_email_confirmation_token(
            self, email_confirmation_token_crud: EmailConfirmationTokenCRUD, test_user: User,
            db_session: AsyncSession,
    ) -> EmailConfirmationToken:
        """A pytest fixture that creates test EmailConfirmationToken object and storing it in the test databases.

        Args:
            email_confirmation_token_crud: instance of database crud logic class.
            user_service: instance of business logic class.
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of EmailConfirmationToken object.
        """
        # Sleeping for N seconds to create different jwt token.
        time.sleep(EmailConfirmationTokenConstants.ONE_SECOND.value)
        jwt_token_payload = create_token_payload(
            data=str(test_user.id),
            time_amount=EmailConfirmationTokenConstants.TOKEN_EXPIRE_7.value,
            time_unit=EmailConfirmationTokenConstants.MINUTES.value,
        )
        jwt_token = create_jwt_token(payload=jwt_token_payload, key=test_user.password)
        db_token = await email_confirmation_token_crud.add_email_confirmation_token(id_=test_user.id, token=jwt_token)
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
            self, change_password_token_crud: ChangePasswordTokenCRUD, user_service: UserService,
            db_session: AsyncSession,
    ) -> ChangePasswordToken:
        """A pytest fixture that creates test ChangePasswordToken object and storing it in the test databases.

        Args:
            change_password_token_crud: instance of database crud logic class.
            user_service: instance of business logic class.
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of EmailConfirmationToken object.
        """
        user = await self._create_user(user_service, UserInputSchema(**request_test_user_data.ADD_USER_TEST_DATA))
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

    @pytest_asyncio.fixture
    async def test_db_expired_change_password_token(
            self,
            test_change_password_token: ChangePasswordToken,
            change_password_token_crud: ChangePasswordTokenCRUD,
            db_session: AsyncSession,
    ) -> ChangePasswordToken:
        """A pytest fixture that creates expired test ChangePasswordToken object and storing it in the test databases.

        Args:
            test_change_password_token: pytest fixture that creates test ChangePasswordToken object.
            change_password_token_crud: instance of database crud logic class.
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        A ChangePasswordToken object with filled 'expired_at' field.
        """
        await change_password_token_crud._expire_change_password_token_by_id(test_change_password_token.id)
        await db_session.refresh(test_change_password_token)
        return test_change_password_token

    @pytest_asyncio.fixture
    async def test_jwt_expired_change_password_token(
            self,
            test_change_password_token: ChangePasswordToken,
            change_password_token_crud: ChangePasswordTokenCRUD,
            db_session: AsyncSession,
    ) -> ChangePasswordToken:
        """A pytest fixture that creates test ChangePasswordToken object with expired jwt token.

        Args:
            test_change_password_token: pytest fixture that creates test ChangePasswordToken object.
            change_password_token_crud: instance of database crud logic class.
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        A ChangePasswordToken object with filled 'expired_at' field.
        """
        jwt_token_payload = create_token_payload(
            data=str(test_change_password_token.user.id),
            time_amount=ChangePasswordTokenConstants.HALF_SECOND.value,
            time_unit=ChangePasswordTokenConstants.SECONDS.value,
        )
        jwt_token = create_jwt_token(payload=jwt_token_payload, key=test_change_password_token.user.password)
        test_change_password_token.token = jwt_token
        db_session.add(test_change_password_token)
        await db_session.commit()
        await db_session.refresh(test_change_password_token)
        return test_change_password_token

    @contextmanager
    def patch_model_time(self, time_to_freeze=None, model=None, field=None, tick=True):
        """Custom context manager that set specified datetime to sqlalchemy model's field.

        Args:
            time_to_freeze: datetime object to set in model's field.
            model: sqlalchemy model object.
            field: sqlalchemy model's field.
            tick: bool.

        Returns:
        An instance of FrozenDateTimeFactory object.
        """
        if not time_to_freeze or not model or not field:
            return
        with freeze_time(time_to_freeze, tick=tick) as frozen_time:
            def set_timestamp(mapper, connection, target):
                now = datetime.now()
                if hasattr(target, field.key):
                    setattr(target, field.key, now)

            event.listen(model, 'before_insert', set_timestamp, propagate=True)
            yield frozen_time
            event.remove(model, 'before_insert', set_timestamp)

    @pytest_asyncio.fixture
    def patch_model_current_time(self):
        """Custom fixture to alter sqlalchemy model's fields with different datetime.

        Returns:
        An instance of FrozenDateTimeFactory object.
        """
        return self.patch_model_time

    @pytest_asyncio.fixture(autouse=True)
    async def charity_service(self, db_session: AsyncSession) -> CharityService:
        """A pytest fixture that creates instance of charity_service business logic.

        Args:
            db_session: pytest fixture that creates test sqlalchemy session.

        Returns:
        An instance of CharityService business logic class.
        """
        return CharityService(session=db_session)

    @pytest_asyncio.fixture
    async def test_charity(
            self, charity_service: CharityService, patch_model_current_time: fixture, request: fixture,
            authenticated_test_user: User,
    ) -> Charity:
        """Create test charity data and store it in test database.

        Args:
            charity_service: instance of business logic class.
            patch_model_current_time: pytest fixture that alters datetime that saves in db model.
            request: native pytest fixture.
            authenticated_test_user: pytest fixture, add user to database and add auth cookies to client fixture.

        Returns:
        newly created Charity object.
        """
        if not hasattr(request, 'param'):
            return await self._create_charity(
                charity_service=charity_service,
                charity=CharityInputSchema(**request_test_charity_data.ADD_CHARITY_TEST_DATA),
                jwt_subject=authenticated_test_user.username,
            )
        with patch_model_current_time(**request.param):
            return await self._create_charity(
                charity_service=charity_service,
                charity=CharityInputSchema(**request_test_charity_data.ADD_CHARITY_TEST_DATA),
                jwt_subject=authenticated_test_user.username,
            )

    async def _create_charity(
            self, charity_service: CharityService, charity: CharityInputSchema, jwt_subject: str,
    ) -> Charity:
        """Stores charity test data in test database.

        Args:
            charity_service: instance of business logic class.
            charity: serialized CharityInputSchema object.
            jwt_subject: decoded jwt identity.

        Returns:
        newly created User object.
        """
        return await charity_service.add_charity(charity=charity, jwt_subject=jwt_subject)

    @pytest_asyncio.fixture
    async def authenticated_random_test_user(
            self, client: fixture, auth_service: AuthService, random_test_user: User,
    ) -> User:
        """Create random authenticated test user data and store it in test database.

        Args:
            client: pytest fixture that creates test httpx client.
            auth_service: instance of auth business logic class.
            random_test_user: pytest fixture, add user with random data to database.

        Returns:
        newly created User object.
        """
        return await self._create_authenticated_user(random_test_user, auth_service, client)

    @pytest_asyncio.fixture
    async def random_test_charity(
            self, charity_service: CharityService, patch_model_current_time: fixture, request: fixture,
            authenticated_random_test_user: User,
    ) -> Charity:
        """Create test charity with random test data and store it in test database.

        Args:
            charity_service: instance of business logic class.
            patch_model_current_time: pytest fixture that alters datetime that saves in db model.
            request: native pytest fixture.
            authenticated_random_test_user: pytest fixture, add user with random data to database and
            auth cookies to client fixture.

        Returns:
        newly created Charity object.
        """
        RANDOM_CHARITY_TEST_DATA = {
            'title': f'Good deeds charity{uuid4()}',
            'description': f'Good deeds charity, making good deeds since 2000 {uuid4()}.',
            'phone_number': f'+38{random.randrange(1000000000, 9999999999)}',
            'email': f'good.deeds{random.randrange(1000000000, 9999999999)}@totalynotemail.com',
        }
        if not hasattr(request, 'param'):
            return await self._create_charity(
                charity_service=charity_service,
                charity=CharityInputSchema(**RANDOM_CHARITY_TEST_DATA),
                jwt_subject=authenticated_random_test_user.username,
            )
        with patch_model_current_time(**request.param):
            return await self._create_charity(
                charity_service=charity_service,
                charity=CharityInputSchema(**RANDOM_CHARITY_TEST_DATA),
                jwt_subject=authenticated_random_test_user.username,
            )
