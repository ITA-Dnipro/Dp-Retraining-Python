import asyncio

from app.celery_base import app
from auth.models import EmailConfirmationToken
from auth.utils.email_confirmation_tokens import EmailConfirmationLambdaClient, EmailConfirmationLetter


@app.task
def send_email_comfirmation_letter(email_confirmation_token: EmailConfirmationToken) -> dict:
    """Background celery task sends to user's email the letter with user profile activation information.

    Args:
        email_confirmation_token: EmailConfirmationToken object instance.

    Returns:
    dict with AWS lambda boto3 ses response.
    """
    email_comfirmation_letter = EmailConfirmationLetter(
        email_confirmation_token=email_confirmation_token,
        server_config=app.conf,
    )
    email_confirmation_lambda_client = EmailConfirmationLambdaClient(
        email_confirmation_letter=email_comfirmation_letter,
        server_config=app.conf,
    )
    return asyncio.run(email_confirmation_lambda_client.send_email())
