from typing import List

from fastapi import FastAPI

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
import pytest

from charity.models import CharityOrganisation
from common.tests.generics import TestMixin
from common.tests.test_data.charity.charity_requests import (
    DUMMY_UUID,
    EDIT_CHARITY,
    EMPTY_REQUEST,
    response_create_organisation_endpoint,
)
from common.tests.test_data.charity.charity_responses import (
    NOT_FOUND,
    NOT_PERMITTED,
    NOT_VALID_REQUEST,
    SUCCESSFUL_CHARITY_DELETION,
    UNAUTHORIZED,
    get_charities_list,
    get_successful_organisation_creating,
    get_successfully_edited_charity_data,
)
from users.models import User


class TestCaseCharity(TestMixin):
    @pytest.mark.asyncio
    async def test_try_to_create_charity_without_auth_should_be_denied(self,
                                                                       app: FastAPI,
                                                                       client: AsyncClient,
                                                                       test_user: User
                                                                       ):
        """
        Test POST '/charities' endpoint with NOT authenticated user.

               Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   test_user: pytest fixture, add user to database.

               Returns:

        """
        url = app.url_path_for('create_charity')
        response = await client.post(url, json=response_create_organisation_endpoint(test_user.id))
        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.json() == UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_create_charity_should_be_ok(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User
    ):
        """
        Test POST '/charities' endpoint with authenticated user.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add user to database and add auth cookies to client fixture.

        Returns:

        """

        url = app.url_path_for('create_charity')
        response = await client.post(url, json=response_create_organisation_endpoint(authenticated_test_user.id))

        response_data = response.json()
        organisation_id = response_data["data"][0]["id"]
        expected_result = get_successful_organisation_creating(organisation_id)
        organisation = (await db_session.execute(select(CharityOrganisation)
                                                 .where(CharityOrganisation.id == organisation_id))).scalar_one()
        assert response.status_code == HTTP_201_CREATED
        assert response_data == expected_result
        assert organisation.users[0].username == "test_john"

    @pytest.mark.asyncio
    async def test_edit_charity_not_authenticated_should_be_denied(self,
                                                                   app: FastAPI,
                                                                   client: AsyncClient,
                                                                   charity: CharityOrganisation
                                                                   ):
        """
        Test PATCH '/charities/{org_id}' endpoint with NOT authenticated user.
        """

        url = app.url_path_for('edit_charity', org_id=charity.id)
        response = await client.patch(url, json=EDIT_CHARITY)
        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.json() == UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_edit_charity_authenticated_should_be_ok(self,
                                                           app: FastAPI,
                                                           client: AsyncClient,
                                                           authenticated_user_charity: CharityOrganisation
                                                           ):
        """
        Test PATCH '/charities/{org_id}' endpoint with authenticated user.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   authenticated_user_charity: pytest fixture, add CharityOrganisation to database
                   and authenticate current user.

        Returns:

        """

        url = app.url_path_for('edit_charity', org_id=authenticated_user_charity.id)
        response = await client.patch(url, json=EDIT_CHARITY)
        assert response.status_code == HTTP_200_OK
        assert response.json() == get_successfully_edited_charity_data(authenticated_user_charity.id)

    @pytest.mark.asyncio
    async def test_pass_empty_request_should_deny(self,
                                                  app: FastAPI,
                                                  client: AsyncClient,
                                                  authenticated_user_charity: CharityOrganisation):
        """
        Test PATCH '/charities/{org_id}' endpoint with authenticated user and empty request.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   authenticated_user_charity: pytest fixture, add CharityOrganisation to database
                   and authenticate current user.

        Returns:

        """

        url = app.url_path_for('edit_charity', org_id=authenticated_user_charity.id)
        response = await client.patch(url, json=EMPTY_REQUEST)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.json() == NOT_VALID_REQUEST

    @pytest.mark.asyncio
    async def test_edit_charity_by_random_user_should_be_forbidden(self,
                                                                   app: FastAPI,
                                                                   client: AsyncClient,
                                                                   charity: CharityOrganisation,
                                                                   authenticated_random_test_user: User
                                                                   ):
        """
        Test PATCH '/charities/{org_id}' endpoint with random authenticated user that is not related to this charity.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity: pytest fixture, add CharityOrganisation to database with non-authenticated user
                   authenticated_random_test_user: pytest fixture, create and authenticate random user which
                   not related to current charity organisation.
        Returns:

        """

        url = app.url_path_for('edit_charity', org_id=charity.id)
        response = await client.patch(url, json=EDIT_CHARITY)
        assert response.status_code == HTTP_403_FORBIDDEN
        assert response.json() == NOT_PERMITTED

    @pytest.mark.asyncio
    async def test_delete_charity_by_random_user_should_be_forbidden(self,
                                                                     app: FastAPI,
                                                                     client: AsyncClient,
                                                                     charity: CharityOrganisation,
                                                                     authenticated_random_test_user: User
                                                                     ):
        """
        Test DELETE '/charities/{org_id}' endpoint with random authenticated user that is not related to this charity.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity: pytest fixture, add CharityOrganisation to database with non-authenticated user
                   authenticated_random_test_user: pytest fixture, create and authenticate random user which
                   not related to current charity organisation.
        Returns:

        """

        url = app.url_path_for('delete_charity', org_id=charity.id)
        response = await client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN
        assert response.json() == NOT_PERMITTED

    @pytest.mark.asyncio
    async def test_delete_charity_authenticated_should_be_ok(self,
                                                             app: FastAPI,
                                                             client: AsyncClient,
                                                             authenticated_user_charity: CharityOrganisation
                                                             ):
        """
        Test DELETE '/charities/{org_id}' endpoint with authenticated user.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   authenticated_user_charity: pytest fixture, add CharityOrganisation to database
                   and authenticate current user.
        Returns:

        """

        url = app.url_path_for('delete_charity', org_id=authenticated_user_charity.id)
        response = await client.delete(url)
        assert response.status_code == HTTP_200_OK
        assert response.json() == SUCCESSFUL_CHARITY_DELETION

    @pytest.mark.asyncio
    async def test_get_definite_should_be_ok(self,
                                             app: FastAPI,
                                             client: AsyncClient,
                                             charity: CharityOrganisation
                                             ):
        """
        Test GET '/charities/{org_id}' endpoint.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity: pytest fixture, add CharityOrganisation to database with non-authenticated user
        Returns:

        """

        url = app.url_path_for('show_charity_organisation', org_id=charity.id)
        response = await client.get(url)
        assert response.status_code == HTTP_200_OK
        assert response.json() == get_charities_list((charity.id,), (charity.title,))

    @pytest.mark.asyncio
    async def test_get_nonexistent_charity_should_not_be_found(self,
                                                               app: FastAPI,
                                                               client: AsyncClient,
                                                               charity: CharityOrganisation
                                                               ):
        """
        Test GET '/charities/{org_id}' endpoint.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity: pytest fixture, add CharityOrganisation to database with non-authenticated user
        Returns:

        """

        url = app.url_path_for('show_charity_organisation', org_id=DUMMY_UUID)
        response = await client.get(url)
        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.json() == NOT_FOUND

    @pytest.mark.asyncio
    async def test_show_existed_charities_should_be_ok(self,
                                                       app: FastAPI,
                                                       client: AsyncClient,
                                                       many_charities: List[CharityOrganisation]
                                                       ):
        """
        Test GET '/charities/' endpoint.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   many_charities: pytest fixture, add CharityOrganisation to database with non-authenticated user
        Returns:

        """

        url = app.url_path_for('show_charities_list')
        response = await client.get(url)
        charity_titles = ("organisation A", "organisation B", "organisation D", "organisation Y")
        charity_ids = []
        charity_phones = []
        charity_mails = []
        for title in charity_titles:
            for charity in many_charities:
                if title == charity.title:
                    charity_ids.append(charity.id)
                    charity_phones.append(charity.phone_number)
                    charity_mails.append(charity.organisation_email)

        assert response.status_code == HTTP_200_OK
        assert response.json() == get_charities_list(charity_ids, charity_titles, charity_phones,charity_mails)
