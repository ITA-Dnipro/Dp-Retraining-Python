from celery.app.utils import Settings
from tenacity import retry, stop_after_attempt, wait_fixed
import httpx

from auth.utils.change_password_tokens import ChangePasswordLetter
from auth.utils.email_confirmation_tokens import EmailConfirmationLetter
from common.constants.auth import EmailLambdaClientConstants
from utils.logging import setup_logging


class EmailLambdaClient:

    def __init__(self, letter: EmailConfirmationLetter | ChangePasswordLetter, server_config: Settings) -> None:
        self.letter = letter
        self._server_config = server_config
        self.client = httpx.AsyncClient()
        self._log = setup_logging(self.__class__.__name__)

    async def send_email(self) -> dict:
        """Makes POST http request to AWS labda that sends email letter.

        Returns:
        Response from boto3 ses client.
        """
        return await self._send_email()

    @retry(
        wait=wait_fixed(EmailLambdaClientConstants.SECOND_1.value),
        stop=stop_after_attempt(EmailLambdaClientConstants.TIMES_5.value),
    )
    async def _send_email(self) -> dict:
        async with self.client as client:
            try:
                response = await client.post(
                    url=self._server_config.get('AWS_EMAIL_LAMBDA_URL'),
                    json=self.letter.payload_data,
                )
            except Exception as exc:
                self._log.warning(exc)
                raise exc
            return response.json()
