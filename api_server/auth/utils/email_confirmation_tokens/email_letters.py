import html
import re

from celery.app.utils import Settings
from jinja2 import Template

from auth.models import EmailConfirmationToken
from common.constants.auth import EmailConfirmationLetterConstants


class EmailConfirmationLetter:

    def __init__(self, email_confirmation_token: EmailConfirmationToken, server_config: Settings) -> None:
        self.email_confirmation_token = email_confirmation_token
        self._server_config = server_config

    @property
    def email_confirmation_url(self):
        return EmailConfirmationLetterConstants.EMAIL_CONFIRMATION_URL.value.format(
            host=self._server_config.get('EMAIL_CONFIRMATION_HOST'),
            port=self._server_config.get('EMAIL_CONFIRMATION_PORT'),
            endpoint=self._server_config.get('EMAIL_CONFIRMATION_ENDPOINT_NAME'),
            token_value_name=self._server_config.get('EMAIL_CONFIRMATION_TOKEN_NAME'),
            token_value=self.email_confirmation_token.token,
        )

    @property
    def front_url(self):
        return EmailConfirmationLetterConstants.FRONT_URL.value.format(
            host=self._server_config.get('EMAIL_CONFIRMATION_HOST'),
            port=self._server_config.get('EMAIL_CONFIRMATION_PORT'),
        )

    @property
    def front_name(self):
        return EmailConfirmationLetterConstants.FRONT_NAME.value

    @property
    def html_template(self):
        email_confirmation_template = Template(EmailConfirmationLetterConstants.EMAIL_HTML_TEMPLATE.value)
        email_confirmation_template = email_confirmation_template.render(
            FRONT_NAME=self.front_name,
            FRONT_URL=self.front_url,
            EMAIL_CONFIRMATION_URL=self.email_confirmation_url,
        )
        email_confirmation_template = re.sub('\n', '', email_confirmation_template)
        email_confirmation_template = html.escape(email_confirmation_template)
        return email_confirmation_template

    @property
    def payload_data(self):
        return {
            'source': self._server_config.get('AWS_SES_EMAIL_SOURCE'),
            'to_address': self.email_confirmation_token.user.email,
            'subject': EmailConfirmationLetterConstants.EMAIL_SUBJECT.value,
            'html': self.html_template,
            'charset': EmailConfirmationLetterConstants.ENCODING_UTF_8.value,
        }
