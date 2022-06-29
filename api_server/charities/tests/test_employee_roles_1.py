from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from charities.models import Charity, CharityEmployeeRoleAssociation, Employee
from charities.tests.test_data import response_charity_employees_test_data, response_employee_roles_test_data
from common.tests.generics import TestMixin
from common.tests.test_data.charities import request_test_charity_employee_data, request_test_employee_role_data
from users.models import User


class TestCaseGetEmployeeRoles(TestMixin):

    @pytest.mark.asyncio
    async def test_get_employee_roles_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
            authenticated_test_user: User,
    ) -> None:
        """Test GET '/charities/{charity_id}/employees/{employee_id}/roles' endpoint with charity, employee and
        employee_role test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for(
            'get_employee_roles',
            charity_id=test_charity.id,
            employee_id=authenticated_test_user.employee.id,
        )
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_employee_roles_test_data.RESPONSE_GET_EMPLOYEE_ROLES_SUPERVISOR_ROLE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_get_employee_roles_invalid_employee_id(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
            authenticated_test_user: User,
    ) -> None:
        """Test GET '/charities/{charity_id}/employees/{employee_id}/roles' endpoint with charity test data added to db
        and invalid dummy 'employee.id'.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for(
            'get_employee_roles',
            charity_id=test_charity.id,
            employee_id=request_test_charity_employee_data.DUMMY_CHARITY_EMPLOYEE_UUID,
        )
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_charity_employees_test_data.RESPONSE_CHARITY_EMPLOYEE_NOT_FOUND_IN_CHARITY
        expected_result['errors'][0]['detail'] = expected_result['errors'][0]['detail'].format(
            charity_id=test_charity.id,
            employee_id=request_test_charity_employee_data.DUMMY_CHARITY_EMPLOYEE_UUID,
        )
        assert response_data == expected_result
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1


class TestCaseGetEmployeeRole(TestMixin):

    @pytest.mark.asyncio
    async def test_get_employee_role_test_data_in_db(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
            authenticated_test_user: User,
    ) -> None:
        """Test GET '/charities/{charity_id}/employees/{employee_id}/roles/{role_id}' endpoint with charity, employee
        and employee_role test data added to the db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for(
            'get_employee_role',
            charity_id=test_charity.id,
            employee_id=authenticated_test_user.employee.id,
            role_id=test_charity.employees[0].roles[0].id,
        )
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_employee_roles_test_data.RESPONSE_GET_EMPLOYEE_ROLE_SUPERVISOR_ROLE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_get_employee_role_invalid_role_id(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
            authenticated_test_user: User,
    ) -> None:
        """Test GET '/charities/{charity_id}/employees/{employee_id}/roles/{role_id}' endpoint with charity test data
        added to db and invalid dummy employee role id.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for(
            'get_employee_role',
            charity_id=test_charity.id,
            employee_id=authenticated_test_user.employee.id,
            role_id=request_test_employee_role_data.DUMMY_EMPLOYEE_ROLE_UUID,
        )
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_employee_roles_test_data.RESPONSE_EMPLOYEE_ROLES_ROLE_NOT_FOUND_IN_EMPLOYEE
        expected_result['errors'][0]['detail'] = expected_result['errors'][0]['detail'].format(
            role_id=request_test_employee_role_data.DUMMY_EMPLOYEE_ROLE_UUID,
            employee_id=authenticated_test_user.employee.id,
        )
        assert response_data == expected_result
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(Employee.id)))).scalar_one() == 1


class TestCasePostEmployeeRoles(TestMixin):

    @pytest.mark.asyncio
    async def test_post_employee_roles_valid_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
            authenticated_test_user: User,
    ) -> None:
        """Test POST '/charities/{charity_id}/employees/{employee_id}/roles' endpoint with charity test data
        added to the db and valid role payload.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.

        Returns:
        Nothing.
        """
        assert (await db_session.execute(select(func.count(CharityEmployeeRoleAssociation.id)))).scalar_one() == 1
        url = app.url_path_for(
            'post_employee_roles',
            charity_id=test_charity.id,
            employee_id=authenticated_test_user.employee.id,
        )
        response = await client.post(url, json=request_test_employee_role_data.ADD_EMPLOYEE_ROLE_MANAGER_TEST_DATA)
        response_data = response.json()
        expected_result = response_employee_roles_test_data.RESPONSE_POST_EMPLOYEE_ROLE_MANAGER_ROLE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(CharityEmployeeRoleAssociation.id)))).scalar_one() == 2

    @pytest.mark.asyncio
    async def test_post_employee_roles_duplicate_creation(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
            authenticated_test_user: User,
    ) -> None:
        """Test POST '/charities/{charity_id}/employees/{employee_id}/roles' endpoint with charity test data
        added to the db and invalid role payload, role already exists.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.

        Returns:
        Nothing.
        """
        assert (await db_session.execute(select(func.count(CharityEmployeeRoleAssociation.id)))).scalar_one() == 1
        url = app.url_path_for(
            'post_employee_roles',
            charity_id=test_charity.id,
            employee_id=authenticated_test_user.employee.id,
        )
        response = await client.post(url, json=request_test_employee_role_data.ADD_EMPLOYEE_ROLE_SUPERVISOR_TEST_DATA)
        response_data = response.json()
        expected_result = response_employee_roles_test_data.RESPONSE_EMPLOYEE_ROLES_SUPERVISOR_ROLE_ALREADY_EXISTS
        expected_result['errors'][0]['detail'] = expected_result['errors'][0]['detail'].format(
            employee_id=authenticated_test_user.employee.id,
        )
        assert response_data == expected_result
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(CharityEmployeeRoleAssociation.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_post_employee_roles_add_not_supported_role(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
            authenticated_test_user: User,
    ) -> None:
        """Test POST '/charities/{charity_id}/employees/{employee_id}/roles' endpoint with charity test data
        added to the db and invalid role payload, not supported role name.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.

        Returns:
        Nothing.
        """
        assert (await db_session.execute(select(func.count(CharityEmployeeRoleAssociation.id)))).scalar_one() == 1
        url = app.url_path_for(
            'post_employee_roles',
            charity_id=test_charity.id,
            employee_id=authenticated_test_user.employee.id,
        )
        response = await client.post(
            url,
            json=request_test_employee_role_data.ADD_EMPLOYEE_ROLE_NOT_SUPPORTED_ROLE_TEST_DATA,
        )
        response_data = response.json()
        expected_result = response_employee_roles_test_data.RESPONSE_EMPLOYEE_ROLES_NOT_SUPPORTED_ROLE
        expected_result['errors'][0]['detail'] = expected_result['errors'][0]['detail'].format(
            role_name=request_test_employee_role_data.ADD_EMPLOYEE_ROLE_NOT_SUPPORTED_ROLE_TEST_DATA['name'],
        )
        assert response_data == expected_result
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(CharityEmployeeRoleAssociation.id)))).scalar_one() == 1


class TestCaseDeleteEmployeeRole(TestMixin):

    @pytest.mark.asyncio
    async def test_delete_employee_roles_employee_only_one_supervisor(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_charity: Charity,
            authenticated_test_user: User,
    ) -> None:
        """Test DELETE '/charities/{charity_id}/employees/{employee_id}/roles/{role_id}' endpoint with charity test data
        added to the db and employee the only one supervisor in charity.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.

        Returns:
        Nothing.
        """
        assert (await db_session.execute(select(func.count(CharityEmployeeRoleAssociation.id)))).scalar_one() == 1
        url = app.url_path_for(
            'delete_employee_role',
            charity_id=test_charity.id,
            employee_id=authenticated_test_user.employee.id,
            role_id=test_charity.employees[0].roles[0].id,
        )
        response = await client.delete(url)
        response_data = response.json()
        expected_result = response_employee_roles_test_data.RESPONSE_EMPLOYEE_ROLES_LAST_SUPERVISOR_IN_CHARITY
        expected_result['errors'][0]['detail'] = expected_result['errors'][0]['detail'].format(
            employee_id=authenticated_test_user.employee.id,
        )
        assert response_data == expected_result
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(CharityEmployeeRoleAssociation.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_delete_employee_roles_valid_data(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, random_test_charity: Charity,
            authenticated_random_test_user: User, test_employee_manager_and_supervisor: Employee,
    ) -> None:
        """Test DELETE '/charities/{charity_id}/employees/{employee_id}/roles/{role_id}' endpoint with charity test data
        added to the db and valid role data.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_charity: pytest fixture, add charity to database.
            authenticated_test_user: pytest fixture, add user to database and auth cookies to client fixture.
            test_employee_manager_and_supervisor: pytest fixture, add supervisor role to employee with manager role in
            random_test_charity.

        Returns:
        Nothing.
        """
        assert (await db_session.execute(select(func.count(CharityEmployeeRoleAssociation.id)))).scalar_one() == 3
        url = app.url_path_for(
            'delete_employee_role',
            charity_id=random_test_charity.id,
            employee_id=test_employee_manager_and_supervisor.id,
            role_id=test_employee_manager_and_supervisor.roles[0].id,
        )
        response = await client.delete(url)
        response_data = response.json()
        expected_result = response_employee_roles_test_data.RESPONSE_DELETE_EMPLOYEE_ROLE
        expected_result['data']['message'] = expected_result['data']['message'].format(
            role_id=test_employee_manager_and_supervisor.roles[0].id,
            employee_id=test_employee_manager_and_supervisor.id,
        )
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(Charity.id)))).scalar_one() == 1
        assert (await db_session.execute(select(func.count(CharityEmployeeRoleAssociation.id)))).scalar_one() == 2
