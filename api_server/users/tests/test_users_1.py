from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from common.tests.generics import TestMixin
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
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, create_user: User,
    ) -> None:
        """Test GET '/users' endpoint with user's test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            create_user: pytest fixture, added to database user.

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
