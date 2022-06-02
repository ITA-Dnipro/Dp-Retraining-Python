import asyncio

from app.celery_base import app
from auth.models import EmailConfirmationToken
from auth.utils.email_confirmation_tokens import EmailConfirmationLetter
from auth.utils.email_lambdas import EmailLambdaClient


@app.task
def send_email_confirmation_letter(email_confirmation_token: EmailConfirmationToken) -> dict:
    """Background celery task sends to user's email the letter with user profile activation information.

    Args:
        email_confirmation_token: EmailConfirmationToken object instance.

    Returns:
    dict with AWS lambda boto3 ses response.
    """
    email_confirmation_letter = EmailConfirmationLetter(
        email_confirmation_token=email_confirmation_token,
        server_config=app.conf,
    )
    email_client = EmailLambdaClient(
        letter=email_confirmation_letter,
        server_config=app.conf,
    )
    return asyncio.run(email_client.send_email())
