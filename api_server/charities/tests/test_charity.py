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

from charities.models import CharityOrganisation
from common.tests.generics import TestMixin
from common.tests.test_data.charity.charity_requests import (
    DUMMY_UUID,
    EDIT_CHARITY,
    EMPTY_REQUEST,
    add_manager_successfully,
    response_create_organisation_endpoint,
)
from common.tests.test_data.charity.charity_responses import (
    NOT_FOUND,
    NOT_PERMITTED,
    NOT_VALID_REQUEST,
    SUCCESSFUL_CHARITY_DELETION,
    SUCCESSFUL_MANAGER_DELETION,
    TITLE_ALREADY_EXISTS,
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
        organisation_id = response_data["data"]["id"]
        expected_result = get_successful_organisation_creating(organisation_id)
        organisation = (await db_session.execute(select(CharityOrganisation)
                                                 .where(CharityOrganisation.id == organisation_id))).scalar_one()
        assert response.status_code == HTTP_201_CREATED
        assert response_data == expected_result
        assert organisation.users[0].username == "test_john"

    @pytest.mark.asyncio
    async def test_edit_charity_not_authenticated_should_be_denied(
            self,
            app: FastAPI,
            client: AsyncClient,
            charity: CharityOrganisation
    ):
        """
        Test PATCH '/charities/{org_id}' endpoint with NOT authenticated user.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            charity: pytest fixture, add CharityOrganisation to database with non-authenticated user

        """

        url = app.url_path_for('edit_charity', org_id=charity.id)
        response = await client.patch(url, json=EDIT_CHARITY)
        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.json() == UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_edit_charity_authenticated_should_be_ok(
            self,
            app: FastAPI,
            client: AsyncClient,
            charity_with_authenticated_director: CharityOrganisation
    ):
        """
        Test PATCH '/charities/{org_id}' endpoint with authenticated user.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity_with_authenticated_director: pytest fixture, add CharityOrganisation to database
                   and authenticate current user.
        Returns:

        """

        url = app.url_path_for('edit_charity', org_id=charity_with_authenticated_director.id)
        response = await client.patch(url, json=EDIT_CHARITY)
        assert response.status_code == HTTP_200_OK
        assert response.json() == get_successfully_edited_charity_data(
            charity_with_authenticated_director.id,
            charity_with_authenticated_director.organisation_email,
            EDIT_CHARITY["phone_number"],
        )

    @pytest.mark.asyncio
    async def test_pass_empty_request_should_deny(
            self,
            app: FastAPI,
            client: AsyncClient,
            charity_with_authenticated_director: CharityOrganisation):
        """
        Test PATCH '/charities/{org_id}' endpoint with authenticated user and empty request.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity_with_authenticated_director: pytest fixture, add CharityOrganisation to database
                   and authenticate current user.

        """

        url = app.url_path_for('edit_charity', org_id=charity_with_authenticated_director.id)
        response = await client.patch(url, json=EMPTY_REQUEST)
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.json() == NOT_VALID_REQUEST

    @pytest.mark.asyncio
    async def test_edit_charity_by_random_user_should_be_forbidden(
            self,
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

        """

        url = app.url_path_for('edit_charity', org_id=charity.id)
        response = await client.patch(url, json=EDIT_CHARITY)
        assert response.status_code == HTTP_403_FORBIDDEN
        assert response.json() == NOT_PERMITTED

    @pytest.mark.asyncio
    async def test_edit_charity_with_duplicate_title_should_be_forbidden(
            self,
            app: FastAPI,
            client: AsyncClient,
            many_charities: List[CharityOrganisation],
    ):
        """
        Test DELETE '/charities/{org_id}' endpoint with random authenticated user that is not related to this charity.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   many_charities: pytest fixture, add CharityOrganisation to database with authenticated director

        """
        charity = None
        for org in many_charities:
            if org.title == "organisation A":
                charity = org
                break
        url = app.url_path_for('edit_charity', org_id=charity.id)
        response = await client.patch(url, json={"title": "organisation B"})
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.json() == TITLE_ALREADY_EXISTS

    @pytest.mark.asyncio
    async def test_delete_charity_by_random_user_should_be_forbidden(
            self,
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
    async def test_delete_charity_authenticated_should_be_ok(
            self,
            app: FastAPI,
            client: AsyncClient,
            charity_with_authenticated_director: CharityOrganisation
    ):
        """
        Test DELETE '/charities/{org_id}' endpoint with authenticated user.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity_with_authenticated_director: pytest fixture, add CharityOrganisation to database
                   and authenticate current user.
        Returns:

        """

        url = app.url_path_for('delete_charity', org_id=charity_with_authenticated_director.id)
        response = await client.delete(url)
        assert response.status_code == HTTP_200_OK
        assert response.json() == SUCCESSFUL_CHARITY_DELETION

    @pytest.mark.asyncio
    async def test_delete_charity_without_director_permission(
            self, app: FastAPI,
            client: AsyncClient,
            charity_with_authenticated_manager: CharityOrganisation):
        """
        Test DELETE '/charities/{org_id}' endpoint.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity_with_authenticated_manager: pytest fixture,
                   add CharityOrganisation to database with non-authenticated user
         """
        url = app.url_path_for('delete_charity', org_id=charity_with_authenticated_manager.id)
        response = await client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN
        assert response.json() == NOT_PERMITTED

    @pytest.mark.asyncio
    async def test_get_definite_charity_should_be_ok(self,
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
        assert response.json()["data"]["description"] == charity.description
        assert response.json()["data"]["id"] == str(charity.id)

    @pytest.mark.asyncio
    async def test_get_nonexistent_charity_should_not_be_found(
            self,
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
    async def test_show_existed_charities_should_be_ok(
            self,
            app: FastAPI,
            client: AsyncClient,
            many_charities: List[CharityOrganisation]
    ):
        """
        Test GET '/charities/' endpoint.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   many_charities: pytest fixture, add CharityOrganisation to database with authenticated director
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
        assert response.json() == get_charities_list(charity_ids, charity_titles, charity_phones, charity_mails)

    @pytest.mark.asyncio
    async def test_add_manager_should_be_ok(
            self,
            app: FastAPI,
            client: AsyncClient,
            charity_with_authenticated_director: CharityOrganisation,
            random_test_user: User):
        """
        Test POST '/charities/{org_id}/managers/add' endpoint. Should be ok because only supermanager or director can
        add new manager.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity_with_authenticated_director: pytest fixture,
                   add CharityOrganisation to database with non-authenticated user
         """
        url = app.url_path_for('add_manager', organisation_id=charity_with_authenticated_director.id)
        response = await client.post(url, json={
            "user_id": str(random_test_user.id),
            "is_supermanager": True
        })
        assert response.status_code == HTTP_200_OK
        assert response.json() == add_manager_successfully(random_test_user.username)

    @pytest.mark.asyncio
    async def test_add_manager_without_supermanager_rights_should_be_denied(
            self,
            app: FastAPI,
            client: AsyncClient,
            charity_with_authenticated_manager: CharityOrganisation,
            random_test_user: User):
        """
        Test POST '/charities/{org_id}/managers/add' endpoint. Should be denied because manager has not
        supermanager rights.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity_with_authenticated_manager: pytest fixture,
                   add CharityOrganisation to database with non-authenticated user
                   random_test_user: pytest fixture, add user with random data to database.
         """
        url = app.url_path_for('add_manager', organisation_id=charity_with_authenticated_manager.id)
        response = await client.post(url, json={
            "user_id": str(random_test_user.id),
            "is_supermanager": True
        })
        assert response.status_code == HTTP_403_FORBIDDEN
        assert response.json() == NOT_PERMITTED

    @pytest.mark.asyncio
    async def test_get_all_managers_of_organisation(
            self,
            app: FastAPI,
            client: AsyncClient,
            charity_with_authenticated_director: CharityOrganisation
    ):
        """
        Test GET '/charities/{org_id}' endpoint.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity_with_authenticated_director: pytest fixture,
                   add CharityOrganisation to database with non-authenticated user
         """
        url = app.url_path_for('show_managers_of_this_organisation',
                               organisation_id=charity_with_authenticated_director.id)
        response = await client.get(url)
        assert response.status_code == HTTP_200_OK
        check_users = []
        users = ["test_john", "test_george"]
        for item in response.json()["data"]:
            check_users.append(item["user"]["username"])
        assert users == check_users

    @pytest.mark.asyncio
    async def test_delete_manager_by_director_should_be_ok(
            self,
            app: FastAPI,
            client: AsyncClient,
            charity_with_authenticated_director: CharityOrganisation):
        """
        Test DELETE '/charities/{org_id}/managers/{user_id}' endpoint. Should be ok because only director
        or supermanager can delete another managers.
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity_with_authenticated_director: pytest fixture,
                   add CharityOrganisation to database with non-authenticated user
         """
        director_id = None
        for user in charity_with_authenticated_director.users_association:
            if user.is_director is True:
                director_id = user.users_id
        url = app.url_path_for('delete_manager_from_organisation', user_id=director_id,
                               organisation_id=charity_with_authenticated_director.id)
        response = await client.delete(url)
        assert response.status_code == HTTP_200_OK
        assert response.json() == SUCCESSFUL_MANAGER_DELETION

    @pytest.mark.asyncio
    async def test_delete_manager_by_another_manager_without_permission_should_be_denied(
            self,
            app: FastAPI,
            client: AsyncClient,
            charity_with_authenticated_manager: CharityOrganisation
    ):
        """
        Test DELETE '/charities/{org_id}/managers/{user_id}' endpoint. Should be denied because only director
        or supermanager can delete another managers. This user has no permission to delete
        Args:
                   app: pytest fixture, an instance of FastAPI.
                   client: pytest fixture, an instance of AsyncClient for http requests.
                   charity_with_authenticated_manager: pytest fixture,
                   add CharityOrganisation to database with non-authenticated user
         """
        user_id = None
        for user in charity_with_authenticated_manager.users:
            if user.username == "test_george":
                user_id = user.id
        url = app.url_path_for('delete_manager_from_organisation', user_id=user_id,
                               organisation_id=charity_with_authenticated_manager.id)
        response = await client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN
        assert response.json() == NOT_PERMITTED
