from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from common.tests.generics import TestMixin
from common.tests.test_data.users import request_test_user_pictures_data
from users.models import User, UserPicture
from users.tests.test_data import response_test_user_pictures_data


class TestCaseGetUserPicture(TestMixin):

    @pytest.mark.asyncio
    async def test_get_user_picture_empty_table(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User,
    ) -> None:
        """Test GET '/users/{user_id}/pictures/{picture_id}' endpoint with no test data added to the UserPicture table.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add user to database and add auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for(
            'get_user_picture',
            user_id=authenticated_test_user.id,
            picture_id=request_test_user_pictures_data.DUMMY_USER_PICTURE_UUID,
        )
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_user_pictures_data.RESPONSE_USER_PICTURE_NOT_FOUND
        assert response_data == expected_result
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (await db_session.execute(select(func.count(UserPicture.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_get_user_picture_(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user_picture: UserPicture,
    ) -> None:
        """Test GET '/users/{user_id}/pictures/{picture_id}' endpoint with test data added to the UserPicture table.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user_picture: pytest fixture, add user picture to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for(
            'get_user_picture',
            user_id=test_user_picture.user_id,
            picture_id=test_user_picture.id,
        )
        response = await client.get(url)
        response_data = response.json()
        expected_result = response_test_user_pictures_data.RESPONSE_GET_USER_PICTURE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(UserPicture.id)))).scalar_one() == 1


class TestCasePostUserPictures(TestMixin):

    @pytest.mark.asyncio
    async def test_post_user_pictures_valid_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, authenticated_test_user: User,
    ) -> None:
        """Test POST '/users/{user_id}/pictures/' endpoint with existing user_id and valid image file.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add user to database and add auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for(
            'post_user_pictures',
            user_id=authenticated_test_user.id,
        )
        response = await client.post(
            url,
            files={'image': request_test_user_pictures_data.TEST_USER_PICTURE_VALID_JPEG},
        )
        response_data = response.json()
        expected_result = response_test_user_pictures_data.RESPONSE_POST_USER_PICTURES
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(UserPicture.id)))).scalar_one() == 1


class TestCaseDeleteUserPicture(TestMixin):

    @pytest.mark.asyncio
    async def test_delete_user_picture_authenticated_user_delete_own_picture(
            self,
            app: FastAPI,
            client: AsyncClient,
            db_session: AsyncSession,
            authenticated_test_user_picture: UserPicture,
    ) -> None:
        """Test DELETE '/users/{user_id}/pictures/{picture_id}' user authenticated and deleting own user picture data.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            authenticated_test_user: pytest fixture, add user to database and add auth cookies to client fixture.

        Returns:
        Nothing.
        """
        url = app.url_path_for(
            'delete_user_picture',
            user_id=authenticated_test_user_picture.user_id,
            picture_id=authenticated_test_user_picture.id,
        )
        response = await client.delete(url)
        response_data = response.content
        expected_result = response_test_user_pictures_data.RESPONSE_USER_PICTURE_DELETE
        assert response_data == expected_result
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert (await db_session.execute(select(func.count(UserPicture.id)))).scalar_one() == 0
