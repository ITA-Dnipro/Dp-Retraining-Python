from celery.app.utils import Settings
from tenacity import retry, stop_after_attempt, wait_fixed
import httpx

from auth.utils.email_confirmation_tokens.email_letters import EmailConfirmationLetter
from common.constants.auth import EmailConfirmationLambdaClientConstants
from utils.logging import setup_logging


class EmailConfirmationLambdaClient:

    def __init__(self, email_confirmation_letter: EmailConfirmationLetter, server_config: Settings) -> None:
        self.email_confirmation_letter = email_confirmation_letter
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
        wait=wait_fixed(EmailConfirmationLambdaClientConstants.WAIT_1_SECOND.value),
        stop=stop_after_attempt(EmailConfirmationLambdaClientConstants.TIMES_5.value),
    )
    async def _send_email(self) -> dict:
        async with self.client as client:
            try:
                response = await client.post(
                    url=self._server_config.get('AWS_EMAIL_CONFIRMATION_LAMBDA_URL'),
                    json=self.email_confirmation_letter.payloda_data,
                )
            except Exception as exc:
                self._log.warning(exc)
                raise exc
            return response.json()
