from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from charities.models import Charity, Employee
from charities.tests.test_data import response_charity_employees_test_data
from common.tests.generics import TestMixin
from common.tests.test_data.charities import request_test_charity_employee_data
from users.models import User


class TestCaseGetCharityEmployees(TestMixin):

    @pytest.mark.asyncio
    async def test_get_charity_employees_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
    ) -> None:
        """Test GET '/charities/{charity_id}/employees' endpoint with charity and employee test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_charity_employees', charity_id=test_charity.id)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_charity_employees_test_data.RESPONSE_GET_CHARITY_EMPLOYEES_SUPERVISOR_ROLE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1


class TestCaseGetCharityEmployee(TestMixin):

    @pytest.mark.asyncio
    async def test_get_charity_employee_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
            authenticated_test_user: User,
    ) -> None:
        """Test GET '/charities/{charity_id}/employees/{employee_id}' endpoint with charity and employee test data
        added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for(
            'get_charity_employee',
            charity_id=test_charity.id,
            employee_id=authenticated_test_user.employee.id,
        )
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_charity_employees_test_data.RESPONSE_GET_CHARITY_EMPLOYEE_SUPERVISOR_ROLE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1


class TestCasePostCharityEmployees(TestMixin):

    @pytest.mark.asyncio
    async def test_post_charity_employees_valid_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, random_test_charity: Charity,
            test_user: User,
    ) -> None:
        """Test POST '/charities/{charity_id}/employees' endpoint with valid payload.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_charity_employees', charity_id=random_test_charity.id)
        response = await client.post(
            url,
            json=request_test_charity_employee_data.ADD_CHARITY_EMPLOYEE_MANAGER_TEST_DATA,
        )
        response_data = response.json()
        expected_result = response_charity_employees_test_data.RESPONSE_POST_CHARITY_EMPLOYEES_MANAGER_ROLE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 2

    @pytest.mark.asyncio
    async def test_post_charity_employees_duplicate_addition(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, random_test_charity: Charity,
            authenticated_random_test_user: User,
    ) -> None:
        """Test POST '/charities/{charity_id}/employees' endpoint with charity employee already added to charity.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.
            authenticated_random_test_user: pytest fixture, add random user to database and auth cookies to client
            fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_charity_employees', charity_id=random_test_charity.id)
        json_payload = request_test_charity_employee_data.ADD_CHARITY_EMPLOYEE_SUPERVISOR_TEST_DATA
        json_payload['user_email'] = authenticated_random_test_user.email
        response = await client.post(
            url,
            json=json_payload,
        )
        response_data = response.json()
        expected_result = response_charity_employees_test_data.RESPONSE_CHARITY_EMPLOYEES_ALREADY_ADDED
        expected_result['errors'][0]['detail'] = expected_result['errors'][0]['detail'].format(
            charity_id=random_test_charity.id,
            employee_id=authenticated_random_test_user.employee.id,
        )
        assert response_data == expected_result
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1
