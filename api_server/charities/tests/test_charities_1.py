from fastapi import FastAPI, status

from httpx import AsyncClient
from pytest import fixture
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from charities.models import Charity, Employee
from charities.tests.test_data import response_charities_test_data
from common.tests.generics import TestMixin
from common.tests.test_data.charities import request_test_charity_data
from common.tests.test_data.users import request_test_user_data
from users.models import User


class TestCaseGetCharities(TestMixin):

    @pytest.mark.asyncio
    async def test_get_charities_empty_db(self, app: FastAPI, client: AsyncClient, db_session: AsyncSession) -> None:
        """Test GET '/charities' endpoint with no charity data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_charities')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_charities_test_data.RESPONSE_GET_CHARITIES_EMPTY_DB
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 0
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_get_charities_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
    ) -> None:
        """Test GET '/charities' endpoint with charity test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_charities')
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_charities_test_data.RESPONSE_GET_CHARITIES
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1


class TestCaseGetCharity(TestMixin):

    @pytest.mark.asyncio
    async def test_get_charity_empty_db(self, app: FastAPI, client: AsyncClient, db_session: AsyncSession) -> None:
        """Test GET '/charities/{id}' endpoint with no charity data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_charity', id=request_test_charity_data.DUMMY_CHARITY_UUID)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_charities_test_data.RESPONSE_CHARITY_NOT_FOUND
        assert response_data == expected_result
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 0
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_get_charity_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
    ) -> None:
        """Test GET '/charities/{id}' endpoint with charity test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_charity', id=test_charity.id)
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_charities_test_data.RESPONSE_GET_CHARITY
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1


class TestCasePostCharities(TestMixin):

    @pytest.mark.asyncio
    async def test_post_charities_valid_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User,
    ) -> None:
        """Test POST '/charities' endpoint with valid payload and no charity data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_charities')
        response = await client.post(url, json=request_test_charity_data.ADD_CHARITY_TEST_DATA)
        response_data = response.json()
        expected_result = response_charities_test_data.RESPONSE_POST_CHARITIES
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_post_charities_duplicate_creation(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
    ) -> None:
        """Test POST '/charities' endpoint with charity data already added to db and valid payload.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_charities')
        response = await client.post(url, json=request_test_charity_data.ADD_CHARITY_TEST_DATA)
        response_data = response.json()
        expected_result = response_charities_test_data.RESPONSE_CHARITY_DUPLICATE_EMAIL
        assert response_data == expected_result
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1


class TestCasePutCharity(TestMixin):

    @pytest.mark.asyncio
    async def test_put_charity_valid_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
    ) -> None:
        """Test PUT '/charities/{id}' endpoint with valid payload and charity data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('put_charity', id=test_charity.id)
        response = await client.put(url, json=request_test_charity_data.UPDATE_CHARITY_TEST_DATA)
        response_data = response.json()
        expected_result = response_charities_test_data.RESPONSE_PUT_CHARITY
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_put_charity_user_updating_charity_where_he_is_not_listed(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, random_test_charity: Charity,
            authenticated_test_user: User,
    ) -> None:
        """Test PUT '/charities/{id}' endpoint with valid payload and user tries to update charity
        where he is not listed as an employee.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            random_test_charity: pytest fixture, add charity with random data to database.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for('put_charity', id=random_test_charity.id)
        response = await client.put(url, json=request_test_charity_data.UPDATE_CHARITY_TEST_DATA)
        response_data = response.json()
        expected_result = response_charities_test_data.RESPONSE_EMPLOYEE_NOT_LISTED_IN_CHARITY_EMPLOYEES
        assert response_data == expected_result
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1


class TestCaseDeleteCharity(TestMixin):

    @pytest.mark.asyncio
    async def test_delete_charity_employee_deleting_own_charity(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
    ) -> None:
        """Test DELETE '/charities/{id}' endpoint, employee listed as 'supervisor' in charity and have permissions.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('delete_charity', id=test_charity.id)
        response = await client.delete(url)
        response_data = response.content
        expected_result = response_charities_test_data.RESPONSE_DELETE_CHARITY
        assert response_data == expected_result
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 0
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_delete_charity_user_deleting_charity_where_he_is_not_listed(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, random_test_charity: Charity,
            authenticated_test_user: User,
    ) -> None:
        """Test DELETE '/charities/{id}' endpoint, user tries to delete charity where he is not listed
        as an employee.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            random_test_charity: pytest fixture, add charity with random data to database.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for('delete_charity', id=random_test_charity.id)
        response = await client.delete(url)
        response_data = response.json()
        expected_result = response_charities_test_data.RESPONSE_EMPLOYEE_NOT_LISTED_IN_CHARITY_EMPLOYEES
        assert response_data == expected_result
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'login_as',
        [{'username': request_test_user_data.ADD_USER_TEST_DATA['username']}],
        indirect=['login_as'],
    )
    async def test_delete_charity_employee_with_manager_role_deleting_own_charity(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, random_test_charity: Charity,
            test_employee_manager: Employee, login_as: fixture,
    ) -> None:
        """Test DELETE '/charities/{id}' endpoint, employee listed as 'manager' in charity and don't have permission to
        delete charity.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            random_test_charity: pytest fixture, add charity with random data to database.
            test_employee_manager: pytest fixture, add employee with manager role to random_test_charity.
            login_as: pytest fixture, finds and authenticate user by provided username.

        Returns:
        Nothing.
        """
        url = app.url_path_for('delete_charity', id=random_test_charity.id)
        response = await client.delete(url)
        response_data = response.json()
        expected_result = response_charities_test_data.RESPONSE_EMPLOYEE_ROLE_MANAGER_NOT_ENOUGH_PERMISSIONS
        assert response_data == expected_result
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 2
