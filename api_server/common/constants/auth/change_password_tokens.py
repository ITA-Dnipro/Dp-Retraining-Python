import enum


class ChangePasswordTokenModelConstants(enum.Enum):
    """ChangePasswordToken model constants."""
    CHAR_SIZE_2048 = 2048


class ChangePasswordTokenSchemaConstants(enum.Enum):
    """ChangePasswordToken schema constants."""
    # Numerics.
    CHAR_SIZE_2 = 2
    CHAR_SIZE_3 = 3
    CHAR_SIZE_6 = 6
    CHAR_SIZE_64 = 64
    CHAR_SIZE_256 = 256
    CHAR_SIZE_2048 = 2048

    # Regex.
    EMAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class ChangePasswordTokenConstants(enum.Enum):
    """EmailConfirmationToken constants."""

    ALGORITHM_HS512 = 'HS512'
    ENCODING_UTF_8 = 'UTF-8'

    # Time units.
    DAYS = 'days'
    MINUTES = 'minutes'
    SECONDS = 'seconds'
    TOKEN_EXPIRE_1 = 1
    ONE_SECOND = 1
    MIN_TOKEN_LIFETIME = 5
    MIN_TOKEN_LIFETIME_TIMEDELTA = {MINUTES: MIN_TOKEN_LIFETIME}
    TIMEDELTA_10_MIN = {MINUTES: 10}

    # Responses.
    SUCCESSFUL_CHANGE_PASSWORD_MSG = {'message': "User with email: '{email}' successfully changed password."}


class ChangePasswordLetterConstants(enum.Enum):
    """ChangePasswordLetter constants."""

    CHANGE_PASSWORD_URL = 'http://www.{host}:{port}/auth/change-password?{token_value_name}={token_value}'
    FRONT_NAME = 'DONATello'
    FRONT_URL = 'http://www.{host}:{port}'
    EMAIL_SUBJECT = 'Change your password.'
    ENCODING_UTF_8 = 'UTF-8'

    EMAIL_HTML_TEMPLATE = '''<!DOCTYPE html>
    <html>
    <head>
    <title>{{FRONT_NAME}} change your password.</title>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
    <meta content="width=device-width" name="viewport">
    <style type="text/css">
        @font-face {
          font-family: &#x27;Postmates Std&#x27;;
          font-weight: 600;
          font-style: normal;
          src: local(&#x27;Postmates Std Bold&#x27;), url(https://s3-us-west-1.amazonaws.com/buyer-static.postmates.com/assets/email/postmates-std-bold.woff) format(&#x27;woff&#x27;);
        }

        @font-face {
          font-family: &#x27;Postmates Std&#x27;;
          font-weight: 500;
          font-style: normal;
          src: local(&#x27;Postmates Std Medium&#x27;), url(https://s3-us-west-1.amazonaws.com/buyer-static.postmates.com/assets/email/postmates-std-medium.woff) format(&#x27;woff&#x27;);
        }

        @font-face {
          font-family: &#x27;Postmates Std&#x27;;
          font-weight: 400;
          font-style: normal;
          src: local(&#x27;Postmates Std Regular&#x27;), url(https://s3-us-west-1.amazonaws.com/buyer-static.postmates.com/assets/email/postmates-std-regular.woff) format(&#x27;woff&#x27;);
        }
    </style>
    <style media="screen and (max-width: 680px)">
        @media screen and (max-width: 680px) {
            .page-center {
              padding-left: 0 !important;
              padding-right: 0 !important;
            }
            
            .footer-center {
              padding-left: 20px !important;
              padding-right: 20px !important;
            }
        }
    </style>
    </head>
    <body style="background-color: #f4f4f5;">
    <table cellpadding="0" cellspacing="0" style="width: 100%; height: 100%; background-color: #f4f4f5; text-align: center;">
    <tbody><tr>
    <td style="text-align: center;">
    <table align="center" cellpadding="0" cellspacing="0" id="body" style="background-color: #fff; width: 100%; max-width: 680px; height: 100%;">
    <tbody><tr>
    <td>
    <table align="center" cellpadding="0" cellspacing="0" class="page-center" style="text-align: left; padding-bottom: 88px; width: 100%; padding-left: 120px; padding-right: 120px;">
    <tbody>
    <tr>
    <td colspan="2" style="padding-top: 72px; -ms-text-size-adjust: 100%; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: 100%; color: #000000; font-family: 'Postmates Std', 'Helvetica', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; font-size: 48px; font-smoothing: always; font-style: normal; font-weight: 600; letter-spacing: -2.6px; line-height: 52px; mso-line-height-rule: exactly; text-decoration: none;">{{FRONT_NAME}}</td>
    </tr>
    <tr>
    <td colspan="2" style="padding-top: 32px; -ms-text-size-adjust: 100%; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: 100%; color: #000000; font-family: 'Postmates Std', 'Helvetica', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; font-size: 38px; font-smoothing: always; font-style: normal; font-weight: 600; letter-spacing: -2.6px; line-height: 52px; mso-line-height-rule: exactly; text-decoration: none;">Change your password</td>
    </tr>
    <tr>
    <td style="padding-top: 32px; padding-bottom: 32px;">
    <table cellpadding="0" cellspacing="0" style="width: 100%">
    <tbody><tr>
    <td style="width: 100%; height: 1px; max-height: 1px; background-color: #d9dbe0; opacity: 0.81"></td>
    </tr>
    </tbody></table>
    </td>
    </tr>
    <tr>
    <td style="-ms-text-size-adjust: 100%; -ms-text-size-adjust: 100%; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: 100%; color: #9095a2; font-family: 'Postmates Std', 'Helvetica', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; font-size: 16px; font-smoothing: always; font-style: normal; font-weight: 400; letter-spacing: -0.18px; line-height: 24px; mso-line-height-rule: exactly; text-decoration: none; vertical-align: top; width: 100%;">
      You're receiving this e-mail because you requested a password change for your {{FRONT_NAME}} account.
    </td>
    </tr>
    <tr>
    <td style="padding-top: 24px; -ms-text-size-adjust: 100%; -ms-text-size-adjust: 100%; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: 100%; color: #9095a2; font-family: 'Postmates Std', 'Helvetica', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; font-size: 16px; font-smoothing: always; font-style: normal; font-weight: 400; letter-spacing: -0.18px; line-height: 24px; mso-line-height-rule: exactly; text-decoration: none; vertical-align: top; width: 100%;">
      Please tap the button below to set up a new password.
    </td>
    </tr>
    <tr>
    <td>
    <a data-click-track-id="37" href="{{CHANGE_PASSWORD_URL}}" style="margin-top: 36px; -ms-text-size-adjust: 100%; -ms-text-size-adjust: 100%; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: 100%; color: #ffffff; font-family: 'Postmates Std', 'Helvetica', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; font-size: 12px; font-smoothing: always; font-style: normal; font-weight: 600; letter-spacing: 0.7px; line-height: 48px; mso-line-height-rule: exactly; text-decoration: none; vertical-align: top; width: 220px; background-color: #00cc99; border-radius: 28px; display: block; text-align: center; text-transform: uppercase" target="_blank">
        Change Password
    </a>
    </td>
    </tr>
    </tbody></table>
    </td>
    </tr>
    </tbody></table>
    <table align="center" cellpadding="0" cellspacing="0" id="footer" style="background-color: #000; width: 100%; max-width: 680px; height: 100%;">
    <tbody><tr>
    <td>
    <table align="center" cellpadding="0" cellspacing="0" class="footer-center" style="text-align: left; width: 100%; padding-left: 120px; padding-right: 120px;">
    <tbody>
    <tr>
    <td colspan="2" style="padding-top: 24px; padding-bottom: 32px;">
    <table cellpadding="0" cellspacing="0" style="width: 100%">
    </table>
    </td>
    </tr>
    <tr>
    <td style="-ms-text-size-adjust: 100%; -ms-text-size-adjust: 100%; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: 100%; color: #9095A2; font-family: 'Postmates Std', 'Helvetica', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif; font-size: 15px; font-smoothing: always; font-style: normal; font-weight: 400; letter-spacing: 0; line-height: 24px; mso-line-height-rule: exactly; text-decoration: none; vertical-align: top; width: 100%;">
    If you didn't request password change you can safely delete this email.
    </td>
    </tr>
    <tr>
    <td style="height: 32px;"></td>
    </tr>
    </tbody></table>
    </td>
    </tr>
    </tbody></table>
    </td>
    </tr>
    </tbody></table>
    </body>
    </html>
    '''# noqa
