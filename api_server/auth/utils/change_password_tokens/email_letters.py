import html
import re

from celery.app.utils import Settings
from jinja2 import Template

from auth.models import ChangePasswordToken
from common.constants.auth import ChangePasswordLetterConstants


class ChangePasswordLetter:

    def __init__(self, db_token: ChangePasswordToken, server_config: Settings) -> None:
        self.db_token = db_token
        self._server_config = server_config

    @property
    def change_password_url(self):
        return ChangePasswordLetterConstants.CHANGE_PASSWORD_URL.value.format(
            host=self._server_config.get('EMAIL_CONFIRMATION_HOST'),
            port=self._server_config.get('EMAIL_CONFIRMATION_PORT'),
            token_value_name=self._server_config.get('EMAIL_CONFIRMATION_TOKEN_NAME'),
            token_value=self.db_token.token,
        )

    @property
    def front_url(self):
        return ChangePasswordLetterConstants.FRONT_URL.value.format(
            host=self._server_config.get('EMAIL_CONFIRMATION_HOST'),
            port=self._server_config.get('EMAIL_CONFIRMATION_PORT'),
        )

    @property
    def front_name(self):
        return ChangePasswordLetterConstants.FRONT_NAME.value

    @property
    def html_template(self):
        change_password_template = Template(ChangePasswordLetterConstants.EMAIL_HTML_TEMPLATE.value)
        change_password_template = change_password_template.render(
            FRONT_NAME=self.front_name,
            FRONT_URL=self.front_url,
            CHANGE_PASSWORD_URL=self.change_password_url,
        )
        change_password_template = re.sub('\n', '', change_password_template)
        change_password_template = html.escape(change_password_template)
        return change_password_template

    @property
    def payloda_data(self):
        return {
            'source': self._server_config.get('AWS_SES_EMAIL_SOURCE'),
            'to_address': self.db_token.user.email,
            'subject': ChangePasswordLetterConstants.EMAIL_SUBJECT.value,
            'html': self.html_template,
            'charset': ChangePasswordLetterConstants.ENCODING_UTF_8.value,
        }
