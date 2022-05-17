from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from balances.models import Balance
from balances.tests.test_data import response_test_balance_data
from common.tests.generics import TestMixin
from common.tests.test_data.balances import request_test_balance_data
from users.models import User


class TestCaseGetBalances(TestMixin):

    @pytest.mark.asyncio
    async def test_get_balances_empty_db(self, app: FastAPI, client: AsyncClient, db_session: AsyncSession) -> None:
        """Test GET '/balances' endpoint with no balance's data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_balances')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_balance_data.RESPONSE_BALANCES_EMPTY_DB
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Balance.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_get_balances_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_balance: Balance,
    ) -> None:
        """Test GET '/balances' endpoint with balance's test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_balance: pytest fixture, add balance to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_balances')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_balance_data.RESPONSE_GET_BALANCES
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Balance.id)))).scalar_one() == 1


class TestCaseGetBalance(TestMixin):

    @pytest.mark.asyncio
    async def test_get_balance_without_access_data(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User
    ) -> None:
        """Test GET '/balances/{id}' endpoint with no balance's data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_balance', id=request_test_balance_data.DUMMY_BALANCE_UUID)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_balance_data.RESPONSE_BALANCE_NO_PERMISSION
        assert response_data == expected_result
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (await db_session.execute(select(func.count(Balance.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_get_balance_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User,
    ) -> None:
        """Test GET '/balances/{id}' endpoint with balance's test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add balance to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_balance', id=authenticated_test_user.balance_id)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_balance_data.RESPONSE_GET_BALANCE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Balance.id)))).scalar_one() == 1
