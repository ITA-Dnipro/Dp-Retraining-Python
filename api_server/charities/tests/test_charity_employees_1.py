from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from charities.models import Charity, Employee
from charities.tests.test_data import response_charity_employees_test_data
from common.tests.generics import TestMixin
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
        expected_result = response_charity_employees_test_data.RESPONSE_GET_CHARITY_EMPLOYEES
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1


class TestCaseGetCharityEmployee(TestMixin):

    @pytest.mark.asyncio
    async def test_get_charity_employe_test_data_in_db(
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
        expected_result = response_charity_employees_test_data.RESPONSE_GET_CHARITY_EMPLOYEE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1
