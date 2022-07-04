from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from common.tests.generics import TestMixin
from common.tests.test_data.fundraisers import request_test_fundraise_data
from fundraisers.models import Fundraise
from fundraisers.tests.test_data import response_fundraisers_test_data


class TestCaseGetFundraisers(TestMixin):

    @pytest.mark.asyncio
    async def test_get_fundraisers_empty_db(self, app: FastAPI, client: AsyncClient, db_session: AsyncSession) -> None:
        """Test GET '/fundraisers' endpoint with no fundraise test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_fundraisers')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_fundraisers_test_data.RESPONSE_GET_FUNDRAISERS_EMPTY_DB
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_get_fundraisers_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_fundraise: Fundraise,
    ) -> None:
        """Test GET '/fundraisers' endpoint with fundraise test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_fundraise: pytest fixture, add fundraise to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_fundraisers')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_fundraisers_test_data.RESPONSE_GET_FUNDRAISERS
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 1


class TestCaseGetFundraise(TestMixin):

    @pytest.mark.asyncio
    async def test_get_fundraise_empty_db(self, app: FastAPI, client: AsyncClient, db_session: AsyncSession) -> None:
        """Test GET '/fundraisers/{id}' endpoint with no fundraise test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_fundraise', id=request_test_fundraise_data.DUMMY_FUNDRAISE_UUID)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_fundraisers_test_data.RESPONSE_FUNDRAISE_NOT_FOUND
        assert response_data == expected_result
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_get_fundraise_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_fundraise: Fundraise,
    ) -> None:
        """Test GET '/fundraisers/{id}' endpoint with fundraise test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_fundraise: pytest fixture, add fundraise to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_fundraise', id=test_fundraise.id)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_fundraisers_test_data.RESPONSE_GET_FUNDRAISE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 1
