import asyncio

from app.celery_base import app
from auth.models import ChangePasswordToken
from auth.utils.change_password_tokens import ChangePasswordLetter
from auth.utils.email_lambdas import EmailLambdaClient


@app.task
def send_change_password_letter(token: ChangePasswordToken) -> dict:
    """Background celery task sends to user's email the letter with link to change user password.

    Args:
        token: ChangePasswordToken object instance.

    Returns:
    dict with AWS lambda boto3 ses response.
    """
    letter = ChangePasswordLetter(
        db_token=token,
        server_config=app.conf,
    )
    email_client = EmailLambdaClient(
        letter=letter,
        server_config=app.conf,
    )
    return asyncio.run(email_client.send_email())
