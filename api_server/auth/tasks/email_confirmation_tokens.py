from app.celery_base import app
from auth.models import EmailConfirmationToken
from auth.utils.email_confirmation_tokens import EmailConfirmationLetter


@app.task
def send_email_comfirmation_letter(email_confirmation_token: EmailConfirmationToken) -> None:
    """Background celery task sends to user's email the letter with user profile activation information.

    Args:
        email_confirmation_token: EmailConfirmationToken object instance.

    Returns:
    Nothing.
    """
    email_comfirmation_letter = EmailConfirmationLetter(
        email_confirmation_token=email_confirmation_token,
        server_config=app.conf,
    )
