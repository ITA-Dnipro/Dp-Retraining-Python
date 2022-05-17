from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from common.tests.generics import TestMixin
from refills.models import Refill
from refills.tests.test_data import response_test_refill_data
from users.models import User


class TestCaseGetRefills(TestMixin):

    @pytest.mark.asyncio
    async def test_get_refills_empty_db(self, app: FastAPI, client: AsyncClient, db_session: AsyncSession) -> None:
        """Test GET '/refills' endpoint with no refill's data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_refills')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_refill_data.RESPONSE_REFILLS_EMPTY_DB
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Refill.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_get_refills_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
            test_refill: Refill,
    ) -> None:
        """Test GET '/refills' endpoint with refill's test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_refill: pytest fixture, add refill to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_refills')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_refill_data.RESPONSE_GET_REFILLS
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Refill.id)))).scalar_one() == 1


class TestCaseGetRefill(TestMixin):

    @pytest.mark.asyncio
    async def test_get_refill_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
            test_refill: Refill, authenticated_test_user: User
    ) -> None:
        """Test GET '/refills/{id}' endpoint with refill's test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add refill to database.

        Returns:
        Nothing.
        """
        refill_id = (await client.get(app.url_path_for('get_refills'))).json()['data'][0]['id']
        url = app.url_path_for('get_refill', id=refill_id)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_refill_data.RESPONSE_GET_REFILL
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Refill.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_get_refill_test_data_empty_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
            authenticated_test_user: User
    ) -> None:
        """Test GET '/refills/{id}' endpoint with refill's test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add refill to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_refill', id=response_test_refill_data.DUMMY_REFILL_UUID)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_refill_data.RESPONSE_REFILL_NOT_FOUND
        assert response_data == expected_result
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (await db_session.execute(select(func.count(Refill.id)))).scalar_one() == 0
