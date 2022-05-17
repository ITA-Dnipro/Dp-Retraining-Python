from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from common.tests.generics import TestMixin
from donations.models import Donation
from donations.tests.test_data import response_test_donation_data


class TestCaseGetDonations(TestMixin):

    @pytest.mark.asyncio
    async def test_get_donations_empty_db(self, app: FastAPI, client: AsyncClient,
                                          db_session: AsyncSession) -> None:
        """Test GET '/donations' endpoint with no donation's data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_donations')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_donation_data.RESPONSE_DONATIONS_EMPTY_DB
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Donation.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_get_donations_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
            test_donation: Donation,
    ) -> None:
        """Test GET '/donations' endpoint with donation's test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_donation: pytest fixture, add donation to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_donations')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_donation_data.RESPONSE_GET_DONATIONS
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Donation.id)))).scalar_one() == 1


class TestCaseGetDonation(TestMixin):

    @pytest.mark.asyncio
    async def test_get_donation_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
            test_donation: Donation,
    ) -> None:
        """Test GET '/donations/{id}' endpoint with donation's test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add donation to database.

        Returns:
        Nothing.
        """
        donation_id = (await client.get(app.url_path_for('get_donations'))).json()['data'][0]['id']
        url = app.url_path_for('get_donation', id=donation_id)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_donation_data.RESPONSE_GET_DONATION
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Donation.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_get_donation_test_data_empty_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
    ) -> None:
        """Test GET '/donations/{id}' endpoint with donation's test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add donation to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_donation', id=response_test_donation_data.DUMMY_DONATION_UUID)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_donation_data.RESPONSE_DONATION_NOT_FOUND
        assert response_data == expected_result
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (await db_session.execute(select(func.count(Donation.id)))).scalar_one() == 0
