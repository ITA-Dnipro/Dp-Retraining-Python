import time

from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from auth.models import ChangePasswordToken
from auth.tests.test_data import response_auth_change_password_data
from common.tests.generics import TestMixin
from common.tests.test_data.auth import request_test_auth_change_password_data
from users.models import User


class TestCasePostAuthForgotPassword(TestMixin):

    @pytest.mark.asyncio
    async def test_post_auth_forgot_password_valid_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test POST '/auth/forgot-password' endpoint with user added to database and valid payload.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_forgot_password')
        response = await client.post(
            url,
            json=request_test_auth_change_password_data.POST_FORGOT_PASSWORD_VALID_EMAIL,
        )
        response_data = response.json()
        expected_result = response_auth_change_password_data.POST_VALID_RESPONSE_FORGOT_PASSWORD_TOKEN_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(ChangePasswordToken.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_post_auth_forgot_password_valid_payload_non_expired_token_alredy_exists(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
            test_change_password_token: ChangePasswordToken,
    ) -> None:
        """Test POST '/auth/forgot-password' endpoint with user added to database and valid payload. Non expired
        change password token already in db.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_change_password_token: pytest fixture, add change password token to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_forgot_password')
        response = await client.post(
            url,
            json=request_test_auth_change_password_data.POST_FORGOT_PASSWORD_VALID_EMAIL,
        )
        response_data = response.json()
        expected_result = response_auth_change_password_data.POST_VALID_RESPONSE_FORGOT_PASSWORD_TOKEN_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(ChangePasswordToken.id)))).scalar_one() == 2
        assert test_change_password_token.expired_at is None
        await db_session.refresh(test_change_password_token)
        assert test_change_password_token.expired_at is not None

    @pytest.mark.asyncio
    async def test_post_auth_forgot_password_valid_payload_2_times_in_row(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test POST '/auth/forgot-password' endpoint with user added to database and valid payload. Making 2 requests
        in a row, first successful and second get anti spam exception.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        # First request.
        url = app.url_path_for('post_forgot_password')
        response = await client.post(
            url,
            json=request_test_auth_change_password_data.POST_FORGOT_PASSWORD_VALID_EMAIL,
        )
        response_data = response.json()
        expected_result = response_auth_change_password_data.POST_VALID_RESPONSE_FORGOT_PASSWORD_TOKEN_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(ChangePasswordToken.id)))).scalar_one() == 1
        # Second request.
        response = await client.post(
            url,
            json=request_test_auth_change_password_data.POST_FORGOT_PASSWORD_VALID_EMAIL,
        )
        response_data = response.json()
        expected_result = response_auth_change_password_data.POST_FORGOT_PASSWORD_ANTI_SPAM_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (await db_session.execute(select(func.count(ChangePasswordToken.id)))).scalar_one() == 1


class TestCasePostAuthChangePassword(TestMixin):

    @pytest.mark.asyncio
    async def test_post_auth_change_password_valid_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
            test_change_password_token: ChangePasswordToken,
    ) -> None:
        """Test POST '/auth/change-password' endpoint with user added to database and valid payload.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_change_password_token: pytest fixture, add change password token to database.

        Returns:
        Nothing.
        """
        assert test_change_password_token.expired_at is None
        user_password_hash_before = test_change_password_token.user.password
        url = app.url_path_for('post_change_password')
        request_test_auth_change_password_data.POST_CHANGE_PASSWORD_VALID_PAYLOAD['token'] = (
            test_change_password_token.token
        )
        response = await client.post(
            url,
            json=request_test_auth_change_password_data.POST_CHANGE_PASSWORD_VALID_PAYLOAD,
        )
        response_data = response.json()
        expected_result = response_auth_change_password_data.POST_VALID_RESPONSE_CHANGE_PASSWORD_TOKEN_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(ChangePasswordToken.id)))).scalar_one() == 1
        await db_session.refresh(test_change_password_token)
        assert test_change_password_token.expired_at is not None
        user_password_hash_after = test_change_password_token.user.password
        assert user_password_hash_before != user_password_hash_after

    @pytest.mark.asyncio
    async def test_post_auth_change_password_with_expired_in_db_token(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
            test_db_expired_change_password_token: ChangePasswordToken,
    ) -> None:
        """Test POST '/auth/change-password' endpoint with user added to database and already expired in db token.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_db_expired_change_password_token: pytest fixture, add expired change password token to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_change_password')
        request_test_auth_change_password_data.POST_CHANGE_PASSWORD_VALID_PAYLOAD['token'] = (
            test_db_expired_change_password_token.token
        )
        response = await client.post(
            url,
            json=request_test_auth_change_password_data.POST_CHANGE_PASSWORD_VALID_PAYLOAD,
        )
        response_data = response.json()
        expected_result = response_auth_change_password_data.POST_CHANGE_PASSWORD_TOKEN_EXPIRED_IN_DB_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (await db_session.execute(select(func.count(ChangePasswordToken.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_post_auth_change_password_with_expired_jwt_token_in_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
            test_jwt_expired_change_password_token: ChangePasswordToken,
    ) -> None:
        """Test POST '/auth/change-password' endpoint with user added to database and already expired in db token.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_jwt_expired_change_password_token: pytest fixture, add expired jwt change password token to database.

        Returns:
        Nothing.
        """
        # Sleeping for N seconds to let jwt token expire.
        time.sleep(1.5)
        assert test_jwt_expired_change_password_token.expired_at is None
        url = app.url_path_for('post_change_password')
        request_test_auth_change_password_data.POST_CHANGE_PASSWORD_VALID_PAYLOAD['token'] = (
            test_jwt_expired_change_password_token.token
        )
        response = await client.post(
            url,
            json=request_test_auth_change_password_data.POST_CHANGE_PASSWORD_VALID_PAYLOAD,
        )
        response_data = response.json()
        expected_result = response_auth_change_password_data.POST_CHANGE_PASSWORD_TOKEN_EXPIRED_IN_JWT_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (await db_session.execute(select(func.count(ChangePasswordToken.id)))).scalar_one() == 1
        await db_session.refresh(test_jwt_expired_change_password_token)
        assert test_jwt_expired_change_password_token.expired_at is not None
