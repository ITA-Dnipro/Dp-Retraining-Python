from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from common.tests.generics import TestMixin
from common.tests.test_data.fundraisers import request_test_fundraise_status_data
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


class TestCasePostFundraiseStatuses(TestMixin):

    @pytest.mark.asyncio
    async def test_post_fundraise_statuses_adding_in_progess_status(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_fundraise: Fundraise,
    ) -> None:
        """Test POST '/fundraisers/{id}/statuses' endpoint with fundraise test data added to the db, adding
        'In progress' status to fundraise.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_fundraise: pytest fixture, add fundraise to database.

        Returns:
        Nothing.
        """
        assert test_fundraise.is_donatable is True
        url = app.url_path_for('post_fundraise_statuses', fundraise_id=test_fundraise.id)
        response = await client.post(
            url,
            json=request_test_fundraise_status_data.ADD_FUNDRAISE_STATUS_IN_PROGRESS_TEST_DATA,
        )
        response_data = response.json()
        expected_result = response_fundraise_statuses_test_data.RESPONSE_POST_FUNDRAISE_STATUS_IN_PROGRESS
        await db_session.refresh(test_fundraise)
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(FundraiseStatusAssociation.id)))).scalar_one() == 2
        assert test_fundraise.is_donatable is True

    @pytest.mark.asyncio
    async def test_post_fundraise_statuses_adding_on_hold_status(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_fundraise: Fundraise,
    ) -> None:
        """Test POST '/fundraisers/{id}/statuses' endpoint with fundraise test data added to the db, adding 'On hold'
        status to fundraise.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_fundraise: pytest fixture, add fundraise to database.

        Returns:
        Nothing.
        """
        assert test_fundraise.is_donatable is True
        url = app.url_path_for('post_fundraise_statuses', fundraise_id=test_fundraise.id)
        response = await client.post(
            url,
            json=request_test_fundraise_status_data.ADD_FUNDRAISE_STATUS_ON_HOLD_TEST_DATA,
        )
        response_data = response.json()
        expected_result = response_fundraise_statuses_test_data.RESPONSE_POST_FUNDRAISE_STATUS_ON_HOLD
        await db_session.refresh(test_fundraise)
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(FundraiseStatusAssociation.id)))).scalar_one() == 2
        assert test_fundraise.is_donatable is False

    @pytest.mark.asyncio
    async def test_post_fundraise_statuses_adding_completed_status(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_fundraise: Fundraise,
    ) -> None:
        """Test POST '/fundraisers/{id}/statuses' endpoint with fundraise test data added to the db, adding 'Completed'
        status to fundraise.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_fundraise: pytest fixture, add fundraise to database.

        Returns:
        Nothing.
        """
        assert test_fundraise.is_donatable is True
        url = app.url_path_for('post_fundraise_statuses', fundraise_id=test_fundraise.id)
        response = await client.post(
            url,
            json=request_test_fundraise_status_data.ADD_FUNDRAISE_STATUS_COMPLETED_TEST_DATA,
        )
        response_data = response.json()
        expected_result = response_fundraise_statuses_test_data.RESPONSE_POST_FUNDRAISE_STATUS_COMPLETED
        await db_session.refresh(test_fundraise)
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(FundraiseStatusAssociation.id)))).scalar_one() == 2
        assert test_fundraise.is_donatable is False

    @pytest.mark.asyncio
    async def test_post_fundraise_statuses_adding_new_status(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_fundraise: Fundraise,
    ) -> None:
        """Test POST '/fundraisers/{id}/statuses' endpoint with fundraise test data added to the db, adding 'New'
        status to fundraise.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_fundraise: pytest fixture, add fundraise to database.

        Returns:
        Nothing.
        """
        assert test_fundraise.is_donatable is True
        url = app.url_path_for('post_fundraise_statuses', fundraise_id=test_fundraise.id)
        response = await client.post(
            url,
            json=request_test_fundraise_status_data.ADD_FUNDRAISE_STATUS_NEW_TEST_DATA,
        )
        response_data = response.json()
        expected_result = response_fundraise_statuses_test_data.RESPONSE_FUNDRAISE_STATUS_NOT_PERMITTED
        await db_session.refresh(test_fundraise)
        assert response_data == expected_result
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(FundraiseStatusAssociation.id)))).scalar_one() == 1
        assert test_fundraise.is_donatable is True

    @pytest.mark.asyncio
    async def test_post_fundraise_statuses_adding_not_supported_status(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_fundraise: Fundraise,
    ) -> None:
        """Test POST '/fundraisers/{id}/statuses' endpoint with fundraise test data added to the db, adding
        'Not supported' status to fundraise.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_fundraise: pytest fixture, add fundraise to database.

        Returns:
        Nothing.
        """
        assert test_fundraise.is_donatable is True
        url = app.url_path_for('post_fundraise_statuses', fundraise_id=test_fundraise.id)
        response = await client.post(
            url,
            json=request_test_fundraise_status_data.ADD_FUNDRAISE_STATUS_NOT_SUPPORTED_TEST_DATA,
        )
        response_data = response.json()
        expected_result = response_fundraise_statuses_test_data.RESPONSE_FUNDRAISE_STATUS_NOT_SUPPORTED
        await db_session.refresh(test_fundraise)
        assert response_data == expected_result
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(FundraiseStatusAssociation.id)))).scalar_one() == 1
        assert test_fundraise.is_donatable is True

    @pytest.mark.asyncio
    async def test_post_fundraise_statuses_adding_on_hold_and_in_progress_statuses(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_fundraise: Fundraise,
    ) -> None:
        """Test POST '/fundraisers/{id}/statuses' endpoint with fundraise test data added to the db, adding 'On hold'
        and then 'In progress' statuses to fundraise.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_fundraise: pytest fixture, add fundraise to database.

        Returns:
        Nothing.
        """
        # Adding 'On hold' status.
        assert test_fundraise.is_donatable is True
        url = app.url_path_for('post_fundraise_statuses', fundraise_id=test_fundraise.id)
        response = await client.post(
            url,
            json=request_test_fundraise_status_data.ADD_FUNDRAISE_STATUS_ON_HOLD_TEST_DATA,
        )
        response_data = response.json()
        expected_result = response_fundraise_statuses_test_data.RESPONSE_POST_FUNDRAISE_STATUS_ON_HOLD
        await db_session.refresh(test_fundraise)
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(FundraiseStatusAssociation.id)))).scalar_one() == 2
        assert test_fundraise.is_donatable is False
        # Adding 'In progress' status.
        response = await client.post(
            url,
            json=request_test_fundraise_status_data.ADD_FUNDRAISE_STATUS_IN_PROGRESS_TEST_DATA,
        )
        response_data = response.json()
        expected_result = response_fundraise_statuses_test_data.RESPONSE_POST_FUNDRAISE_STATUS_IN_PROGRESS
        await db_session.refresh(test_fundraise)
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(Fundraise.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(FundraiseStatusAssociation.id)))).scalar_one() == 3
        assert test_fundraise.is_donatable is True
