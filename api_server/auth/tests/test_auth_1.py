from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from auth.tests.test_data import response_auth_test_data
from common.tests.generics import TestMixin
from common.tests.test_data.auth import request_test_auth_data
from users.models import User


class TestCasePostAuthLogin(TestMixin):

    @pytest.mark.asyncio
    async def test_post_auth_login_valid_credentials(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test POST '/auth/login' endpoint with user added to database and valid credentials.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('login')
        response = await client.post(url, json=request_test_auth_data.LOGIN_VALID_USER_CREDENTIALS)
        response_data = response.json()
        expected_result = response_auth_test_data.RESPONSE_VALID_LOGIN_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_post_auth_login_invalid_credentials(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test POST '/auth/login' endpoint with user added to database and invalid credentials, wrong password.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('login')
        response = await client.post(url, json=request_test_auth_data.LOGIN_INVALID_USER_PASSWORD)
        response_data = response.json()
        expected_result = response_auth_test_data.RESPONSE_INVALID_LOGIN_PASSWORD
        assert response_data == expected_result
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1


class TestCasePostAuthMe(TestMixin):

    @pytest.mark.asyncio
    async def test_post_auth_me_valid_auth_cookies(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User,
    ) -> None:
        """Test POST '/auth/me' endpoint with user added to database and auth cookies present in request.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add user to database and add auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for('auth_me')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_auth_test_data.RESPONSE_VALID_ME_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_post_auth_me_no_auth_cookies(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test POST '/auth/me' endpoint with user added to database and no auth cookies in request.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('auth_me')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_auth_test_data.RESPONSE_NO_ACCESS_COOKIES
        assert response_data == expected_result
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1


class TestCasePostAuthLogout(TestMixin):

    @pytest.mark.asyncio
    async def test_post_auth_logout_valid_auth_cookies(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User,
    ) -> None:
        """Test POST '/auth/logout' endpoint with user added to database and auth cookies present in request.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add user to database and add auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for('logout')
        response = await client.post(url)
        response_data = response.json()
        expected_result = response_auth_test_data.RESPONSE_POST_VALID_LOGOUT
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_post_auth_logout_no_auth_cookies(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test POST '/auth/logout' endpoint with user added to database and no auth cookies in request.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('logout')
        response = await client.post(url)
        response_data = response.json()
        expected_result = response_auth_test_data.RESPONSE_NO_ACCESS_COOKIES
        assert response_data == expected_result
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1


class TestCasePostAuthRefresh(TestMixin):

    @pytest.mark.asyncio
    async def test_post_auth_refresh_valid_auth_cookies(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User,
    ) -> None:
        """Test POST '/auth/refresh' endpoint with user added to database and auth cookies present in request.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add user to database and add auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for('refresh')
        response = await client.post(url)
        response_data = response.json()
        expected_result = response_auth_test_data.RESPONSE_VALID_REFRESH_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_post_auth_refresh_no_auth_cookies(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test POST '/auth/refresh' endpoint with user added to database and no auth cookies in request.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('refresh')
        response = await client.post(url)
        response_data = response.json()
        expected_result = response_auth_test_data.RESPONSE_NO_REFRESH_COOKIES
        assert response_data == expected_result
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert (await db_session.execute(select(func.count(User.id)))).scalar_one() == 1
