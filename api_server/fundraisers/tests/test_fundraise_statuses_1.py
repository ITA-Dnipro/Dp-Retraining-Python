from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from common.tests.generics import TestMixin
from fundraisers.models import Fundraise, FundraiseStatusAssociation
from fundraisers.tests.test_data import response_fundraise_statuses_test_data


class TestCaseGetFundraiseStatuses(TestMixin):

    @pytest.mark.asyncio
    async def test_get_fundraise_statuses_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_fundraise: Fundraise
    ) -> None:
        """Test GET '/fundraisers/{id}/statuses' endpoint with fundraise and status test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_fundraise: pytest fixture, add fundraise to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_fundraise_statuses', fundraise_id=test_fundraise.id)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_fundraise_statuses_test_data.RESPONSE_GET_FUNDRAISE_STATUSES
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(FundraiseStatusAssociation.id)))).scalar_one() == 1


class TestCaseGetFundraiseStatus(TestMixin):

    @pytest.mark.asyncio
    async def test_get_fundraise_status_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_fundraise: Fundraise
    ) -> None:
        """Test GET '/fundraisers/{fundraise_id}/statuses/{status_id}' endpoint with fundraise and status test data
        added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_fundraise: pytest fixture, add fundraise to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for(
            'get_fundraise_status',
            fundraise_id=test_fundraise.id,
            status_id=test_fundraise.statuses[0].id,
        )
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_fundraise_statuses_test_data.RESPONSE_GET_FUNDRAISE_STATUS
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(FundraiseStatusAssociation.id)))).scalar_one() == 1
