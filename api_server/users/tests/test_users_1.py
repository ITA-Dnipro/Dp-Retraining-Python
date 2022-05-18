import pytest
from common.tests.generics import TestMixin
from common.tests.test_data.users import request_test_user_data
from fastapi import FastAPI, status
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import User
from users.tests.test_data import response_test_user_data


class TestCaseGetUsers(TestMixin):

    @pytest.mark.asyncio
    async def test_get_users_empty_db(self, app: FastAPI, client: AsyncClient, db_session: AsyncSession) -> None:
        """Test GET '/users' endpoint with no user's data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_users')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_user_data.RESPONSE_USERS_EMPTY_DB
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_get_users_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test GET '/users' endpoint with user's test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_users')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_user_data.RESPONSE_GET_USERS
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1


class TestCaseGetUser(TestMixin):

    @pytest.mark.asyncio
    async def test_get_user_no_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
    ) -> None:
        """Test GET '/users/{id}' endpoint with no user's data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_user', id=request_test_user_data.DUMMY_USER_UUID)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_user_data.RESPONSE_USER_NOT_FOUND
        assert response_data == expected_result
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_get_user_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test GET '/users/{id}' endpoint with user's test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_user', id=test_user.id)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_user_data.RESPONSE_GET_USER
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1


class TestCasePostUsers(TestMixin):

    @pytest.mark.asyncio
    async def test_post_users_valid_payload(self, app: FastAPI, client: AsyncClient, db_session: AsyncSession) -> None:
        """Test POST '/users' endpoint with valid payload and no user's data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_users')
        response = await client.post(url, json=request_test_user_data.ADD_USER_TEST_DATA)
        response_data = response.json()
        expected_result = response_test_user_data.RESPONSE_POST_USER
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_post_users_invalid_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
    ) -> None:
        """Test POST '/users' endpoint with invalid empty payload.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_users')
        response = await client.post(url, json=request_test_user_data.ADD_USER_EMPTY_TEST_DATA)
        response_data = response.json()
        expected_result = response_test_user_data.RESPONSE_USER_INVALID_PAYLOAD
        assert response_data == expected_result
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_post_users_duplicate_creation(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test POST '/users' endpoint with user already present in database.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_users')
        response = await client.post(url, json=request_test_user_data.ADD_USER_TEST_DATA)
        response_data = response.json()
        expected_result = response_test_user_data.RESPONSE_USER_DUPLICATE_USERNAME
        assert response_data == expected_result
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1


class TestCasePutUser(TestMixin):

    @pytest.mark.asyncio
    async def test_put_user_valid_payload_updating_himself(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User,
    ) -> None:
        """Test PUT '/users/{id}' endpoint with valid payload user authenticated and updating own data.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add user to database and add auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for('put_user', id=authenticated_test_user.id)
        response = await client.put(url, json=request_test_user_data.UPDATE_USER_TEST_DATA)
        response_data = response.json()
        expected_result = response_test_user_data.RESPONSE_USER_UPDATE_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_put_user_updating_other_user_data(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User,
            random_test_user: User,
    ) -> None:
        """Test PUT '/users/{id}' endpoint with valid payload user authenticated and updating other user data.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add user to database and add auth cookies to client fixture.
            random_test_user: pytest fixture, add user with random data to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('put_user', id=random_test_user.id)
        response = await client.put(url, json=request_test_user_data.UPDATE_USER_TEST_DATA)
        response_data = response.json()
        expected_result = response_test_user_data.RESPONSE_USER_UNAUTHORIZED_UPDATE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 2


class TestCaseDeleteUser(TestMixin):

    @pytest.mark.asyncio
    async def test_delete_user_authenticated_deleting_himself(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User,
    ) -> None:
        """Test DELETE '/users/{id}' endpoint user authenticated and deleting own data.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add user to database and add auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for('delete_user', id=authenticated_test_user.id)
        response = await client.delete(url)
        response_data = response.content
        expected_result = response_test_user_data.RESPONSE_USER_DELETE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_delete_user_authenticated_deleting_other_user_data(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User,
            random_test_user: User,
    ) -> None:
        """Test DELETE '/users/{id}' endpoint user authenticated and deleting other user data.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add user to database and add auth cookies to client fixture.
            random_test_user: pytest fixture, add user with random data to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('delete_user', id=random_test_user.id)
        response = await client.delete(url)
        response_data = response.json()
        expected_result = response_test_user_data.RESPONSE_USER_UNAUTHORIZED_DELETE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 2
