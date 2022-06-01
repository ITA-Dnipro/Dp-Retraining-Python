import time

from fastapi import FastAPI, status

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
import pytest

from auth.models import EmailConfirmationToken
from auth.tests.test_data import response_auth_email_confirmation_data
from common.constants.auth import EmailConfirmationTokenConstants
from common.tests.generics import TestMixin
from common.tests.test_data.auth import request_test_auth_email_confirmation_data
from users.models import User


class TestCasePostAuthEmailConfirmation(TestMixin):

    @pytest.mark.asyncio
    async def test_post_auth_email_confirmation_valid_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test POST '/auth/email-confirmation' endpoint with user added to database and valid payload.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_user_email_confirmation')
        response = await client.post(
            url,
            json=request_test_auth_email_confirmation_data.POST_EMAIL_CONFIRMATION_VALID_EMAIL,
        )
        response_data = response.json()
        expected_result = response_auth_email_confirmation_data.POST_VALID_RESPONSE_EMAIL_CONFIRMATION_TOKEN_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(EmailConfirmationToken.id)))).scalar_one() == 1

    @pytest.mark.asyncio
    async def test_post_auth_email_confirmation_valid_payload_non_expired_token_already_exists(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
            test_email_confirmation_token: EmailConfirmationToken,
    ) -> None:
        """Test POST '/auth/email-confirmation' endpoint with user added and non expired token already in db.
        New token gets created, old one gets expired.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_email_confirmation_token: pytest fixture, add email confirmation token to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_user_email_confirmation')
        # Sleeping for N seconds to create different jwt token from pytest fixture.
        time.sleep(EmailConfirmationTokenConstants.ONE_SECOND.value)
        response = await client.post(
            url,
            json=request_test_auth_email_confirmation_data.POST_EMAIL_CONFIRMATION_VALID_EMAIL,
        )
        response_data = response.json()
        expected_result = response_auth_email_confirmation_data.POST_VALID_RESPONSE_EMAIL_CONFIRMATION_TOKEN_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(EmailConfirmationToken.id)))).scalar_one() == 2
        assert test_email_confirmation_token.expired_at is None
        await db_session.refresh(test_email_confirmation_token)
        assert test_email_confirmation_token.expired_at is not None

    @pytest.mark.asyncio
    async def test_post_auth_email_confirmation_invalid_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test POST '/auth/email-confirmation' endpoint with user added and invalid user's email in payload.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_user: pytest fixture, add user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('post_user_email_confirmation')
        response = await client.post(
            url,
            json=request_test_auth_email_confirmation_data.POST_EMAIL_CONFIRMATION_INVALID_EMAIL,
        )
        response_data = response.json()
        expected_result = response_auth_email_confirmation_data.RESPONSE_EMAIL_CONFIRMATION_USER_EMAIL_NOT_FOUND
        assert response_data == expected_result
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert (await db_session.execute(select(func.count(EmailConfirmationToken.id)))).scalar_one() == 0

    @pytest.mark.asyncio
    async def test_post_auth_email_confirmation_valid_payload_2_times_in_row(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession, test_user: User,
    ) -> None:
        """Test POST '/auth/email-confirmation' endpoint with user added to database and valid payload.Making 2 requests
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
        url = app.url_path_for('post_user_email_confirmation')
        response = await client.post(
            url,
            json=request_test_auth_email_confirmation_data.POST_EMAIL_CONFIRMATION_VALID_EMAIL,
        )
        response_data = response.json()
        expected_result = response_auth_email_confirmation_data.POST_VALID_RESPONSE_EMAIL_CONFIRMATION_TOKEN_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_201_CREATED
        assert (await db_session.execute(select(func.count(EmailConfirmationToken.id)))).scalar_one() == 1
        # Second request.
        url = app.url_path_for('post_user_email_confirmation')
        response = await client.post(
            url,
            json=request_test_auth_email_confirmation_data.POST_EMAIL_CONFIRMATION_VALID_EMAIL,
        )
        response_data = response.json()
        expected_result = response_auth_email_confirmation_data.POST_EMAIL_CONFIRMATION_ANTI_SPAM_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (await db_session.execute(select(func.count(EmailConfirmationToken.id)))).scalar_one() == 1


class TestCaseGetAuthEmailConfirmation(TestMixin):

    @pytest.mark.asyncio
    async def test_get_auth_email_confirmation_valid_payload(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
            test_email_confirmation_token: EmailConfirmationToken,
    ) -> None:
        """Test GET '/auth/email-confirmation' endpoint with user added and valid payload. User gets activated and
        current EmailConfirmationToken expired.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_email_confirmation_token: pytest fixture, add email confirmation token to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_user_email_confiramation')
        request_test_auth_email_confirmation_data.GET_EMAIL_CONFIRMATION_VALID_TOKEN['token'] = (
            test_email_confirmation_token.token
        )
        response = await client.get(
            url,
            params=request_test_auth_email_confirmation_data.GET_EMAIL_CONFIRMATION_VALID_TOKEN,
        )
        response_data = response.json()
        expected_result = response_auth_email_confirmation_data.GET_VALID_RESPONSE_EMAIL_CONFIRMATION_TOKEN_TEST_DATA
        assert response_data == expected_result
        assert response.status_code == status.HTTP_200_OK
        assert (await db_session.execute(select(func.count(EmailConfirmationToken.id)))).scalar_one() == 1
        assert test_email_confirmation_token.expired_at is None
        assert test_email_confirmation_token.user.activated_at is None
        await db_session.refresh(test_email_confirmation_token)
        assert test_email_confirmation_token.expired_at is not None
        assert test_email_confirmation_token.user.activated_at is not None

    @pytest.mark.asyncio
    async def test_get_auth_email_confirmation_user_already_activated(
            self, app: FastAPI, client: AsyncClient, db_session: AsyncSession,
            test_activated_email_confirmation_token: EmailConfirmationToken,
    ) -> None:
        """Test GET '/auth/email-confirmation' endpoint with user added and already activated.

        Args:
            app: pytest fixture, an instance of FastAPI.
            client: pytest fixture, an instance of AsyncClient for http requests.
            db_session: pytest fixture, sqlalchemy AsyncSession.
            test_activated_user: pytest fixture, add activated user to database.

        Returns:
        Nothing.
        """
        url = app.url_path_for('get_user_email_confiramation')
        request_test_auth_email_confirmation_data.GET_EMAIL_CONFIRMATION_VALID_TOKEN['token'] = (
            test_activated_email_confirmation_token.token
        )
        response = await client.get(
            url,
            params=request_test_auth_email_confirmation_data.GET_EMAIL_CONFIRMATION_VALID_TOKEN,
        )
        response_data = response.json()
        expected_result = response_auth_email_confirmation_data.GET_EMAIL_CONFIRMATION_USER_ALREADY_ACTIVATED
        assert response_data == expected_result
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (await db_session.execute(select(func.count(EmailConfirmationToken.id)))).scalar_one() == 1
        assert test_activated_email_confirmation_token.expired_at is not None
        assert test_activated_email_confirmation_token.user.activated_at is not None
