from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from charities.models import Charity
from common.tests.generics import TestMixin
from common.tests.test_data.fundraisers import request_test_fundraise_data
from fundraisers.models import Fundraise
from fundraisers.tests.test_data import response_fundraisers_test_data
from users.models import User


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


class TestCasePostFundraisers(TestMixin):

    @pytest.mark.asyncio
    async def test_post_fundraisers_valid_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
    ) -> None:
        """Test POST '/fundraisers' endpoint with valid payload and no fundraise test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.

        Returns:
        Nothing.
        """
        payload = request_test_fundraise_data.ADD_FUNDRAISE_TEST_DATA
        payload['charity_id'] = str(test_charity.id)
        url = app.url_path_for('post_fundraisers')
        response = await client.post(url, json=payload)
        response_data = response.json()
        expected_result = response_fundraisers_test_data.RESPONSE_POST_FUNDRAISE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_post_fundraisers_employee_adding_fundraise_to_other_charity(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, random_test_charity: Charity,
            authenticated_test_user: User,
    ) -> None:
        """Test POST '/fundraisers' endpoint with valid payload and employee tries to create fundraise withing charity
        where he is not listed as employee.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            random_test_charity: pytest fixture, add charity with random data to database.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.

        Returns:
        Nothing.
        """
        payload = request_test_fundraise_data.ADD_FUNDRAISE_TEST_DATA
        payload['charity_id'] = str(random_test_charity.id)
        url = app.url_path_for('post_fundraisers')
        response = await client.post(url, json=payload)
        response_data = response.json()
        expected_result = response_fundraisers_test_data.RESPONSE_FUNDRAISE_NO_EMPLOYEE_PERMISSION
        assert response_data == expected_result
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 0
