import enum


class EmailConfirmationTokenModelConstants(enum.Enum):
    """EmailConfirmationToken model constants."""
    CHAR_SIZE_2048 = 2048


class EmailConfirmationTokenSchemaConstants(enum.Enum):
    """EmailConfirmationToken schema constants."""
    # Numerics.
    CHAR_SIZE_2 = 2
    CHAR_SIZE_3 = 3
    CHAR_SIZE_6 = 6
    CHAR_SIZE_64 = 64
    CHAR_SIZE_256 = 256
    CHAR_SIZE_2048 = 2048

    # Regex.
    EMAIL_REGEX = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'


class JWTTokenConstants(enum.Enum):
    """Generic JWT token constants."""

    ALGORITHM_HS512 = 'HS512'
    ENCODING_UTF_8 = 'UTF-8'


class EmailConfirmationTokenConstants(enum.Enum):
    """EmailConfirmationToken constants."""

    # Time units.
    DAYS = 'days'
    MINUTES = 'minutes'
    SECONDS = 'seconds'
    TOKEN_EXPIRE_7 = 7
    ONE_SECOND = 1
    MIN_TOKEN_LIFETIME = 5
    MIN_TOKEN_LIFETIME_TIMEDELTA = {MINUTES: MIN_TOKEN_LIFETIME}
    TIMEDELTA_10_MIN = {MINUTES: 10}
    TIMEDELTA_30_MIN = {MINUTES: 30}

    # Responses.
    SUCCESSFUL_EMAIL_CONFIRMATION_MSG = {'message': "User with email: '{email}' successfully activated."}


class EmailConfirmationLetterConstants(enum.Enum):
    """EmailConfirmationLetter constants."""

    EMAIL_CONFIRMATION_URL = 'http://www.{host}:{port}{endpoint}?{token_value_name}={token_value}'
    FRONT_NAME = 'DONATello'
    FRONT_URL = 'http://www.{host}:{port}'
    EMAIL_SUBJECT = 'Please, verify your email address.'
    ENCODING_UTF_8 = 'UTF-8'
    EMAIL_HTML_TEMPLATE = '''<!DOCTYPE html>
    <html>
    <head>

      <meta charset="utf-8">
      <meta http-equiv="x-ua-compatible" content="ie=edge">
      <title>Email Confirmation</title>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <style type="text/css">
      /**
      * Google webfonts. Recommended to include the .woff version for cross-client compatibility.
      */
      @media screen {
        @font-face {
          font-family: 'Source Sans Pro';
          font-style: normal;
          font-weight: 400;
          src: local('Source Sans Pro Regular'), local('SourceSansPro-Regular'), url(https://fonts.gstatic.com/s/sourcesanspro/v10/ODelI1aHBYDBqgeIAH2zlBM0YzuT7MdOe03otPbuUS0.woff) format('woff');
        }
        @font-face {
          font-family: 'Source Sans Pro';
          font-style: normal;
          font-weight: 700;
          src: local('Source Sans Pro Bold'), local('SourceSansPro-Bold'), url(https://fonts.gstatic.com/s/sourcesanspro/v10/toadOcfmlt9b38dHJxOBGFkQc6VGVFSmCnC_l7QZG60.woff) format('woff');
        }
      }
      /**
      * Avoid browser level font resizing.
      * 1. Windows Mobile
      * 2. iOS / OSX
      */
      body,
      table,
      td,
      a {
        -ms-text-size-adjust: 100%; /* 1 */
        -webkit-text-size-adjust: 100%; /* 2 */
      }
      /**
      * Remove extra space added to tables and cells in Outlook.
      */
      table,
      td {
        mso-table-rspace: 0pt;
        mso-table-lspace: 0pt;
      }
      /**
      * Better fluid images in Internet Explorer.
      */
      img {
        -ms-interpolation-mode: bicubic;
      }
      /**
      * Remove blue links for iOS devices.
      */
      a[x-apple-data-detectors] {
        font-family: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
        line-height: inherit !important;
        color: inherit !important;
        text-decoration: none !important;
      }
      /**
      * Fix centering issues in Android 4.4.
      */
      div[style*="margin: 16px 0;"] {
        margin: 0 !important;
      }
      body {
        width: 100% !important;
        height: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
      }
      /**
      * Collapse table borders to avoid space between cells.
      */
      table {
        border-collapse: collapse !important;
      }
      a {
        color: #1a82e2;
      }
      img {
        height: auto;
        line-height: 100%;
        text-decoration: none;
        border: 0;
        outline: none;
      }
      </style>

    </head>
    <body style="background-color: #e9ecef;">

      <!-- start preheader -->
      <div class="preheader" style="display: none; max-width: 0; max-height: 0; overflow: hidden; font-size: 1px; line-height: 1px; color: #fff; opacity: 0;">
        ???? ???? ???? ???? ???? ???? ??? ??? ??? Welcome to DONATello please confirm your email address. ???? ???? ???? ???? ???? ???? ??? ??? ???
      </div>
      <!-- end preheader -->

      <!-- start body -->
      <table border="0" cellpadding="0" cellspacing="0" width="100%">

        <!-- start logo -->
        <tr>
          <td align="center" bgcolor="#e9ecef">
            <!--[if (gte mso 9)|(IE)]>
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
            <tr>
            <td align="center" valign="top" width="600">
            <![endif]-->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
              <tr>
                <td align="center" valign="top" style="padding: 36px 24px;">
                  <h1 style="margin: 0; 
                            font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 48px;">Welcome to {{FRONT_NAME}}</h1>
                </td>
              </tr>
            </table>
            <!--[if (gte mso 9)|(IE)]>
            </td>
            </tr>
            </table>
            <![endif]-->
          </td>
        </tr>
        <!-- end logo -->

        <!-- start hero -->
        <tr>
          <td align="center" bgcolor="#e9ecef">
            <!--[if (gte mso 9)|(IE)]>
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
            <tr>
            <td align="center" valign="top" width="600">
            <![endif]-->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">
              <tr>
                <td align="left" bgcolor="#ffffff" style="padding: 36px 24px 0; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; border-top: 3px solid #d4dadf;">
                  <h5 style="margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 48px;">Confirm Your Email Address</h5>
                </td>
              </tr>
            </table>
            <!--[if (gte mso 9)|(IE)]>
            </td>
            </tr>
            </table>
            <![endif]-->
          </td>
        </tr>
        <!-- end hero -->

        <!-- start copy block -->
        <tr>
          <td align="center" bgcolor="#e9ecef">
            <!--[if (gte mso 9)|(IE)]>
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
            <tr>
            <td align="center" valign="top" width="600">
            <![endif]-->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">

              <!-- start copy -->
              <tr>
                <td align="left" bgcolor="#ffffff" style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px;">
                  <p style="margin: 0;">Tap the button below to confirm your email address. If you didn't create an account with <a href="{{FRONT_URL}}" target="_blank">{{FRONT_NAME}}</a>, you can safely delete this email.</p>
                </td>
              </tr>
              <!-- end copy -->

              <!-- start button -->
              <tr>
                <td align="left" bgcolor="#ffffff">
                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                      <td align="center" bgcolor="#ffffff" style="padding: 12px;">
                        <table border="0" cellpadding="0" cellspacing="0">
                          <tr>
                            <td align="center" bgcolor="#1a82e2" style="border-radius: 6px;">
                              <a href="{{EMAIL_CONFIRMATION_URL}}" target="_blank" style="display: inline-block; padding: 16px 36px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; color: #ffffff; text-decoration: none; border-radius: 6px;">Confirm email address</a>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
              <!-- end button -->

              <!-- start copy -->
              <tr>
                <td align="left" bgcolor="#ffffff" style="padding: 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px; border-bottom: 3px solid #d4dadf">
                  <p style="margin: 0;">Cheers,<br>{{FRONT_NAME}}</p>
                </td>
              </tr>
              <!-- end copy -->

            </table>
            <!--[if (gte mso 9)|(IE)]>
            </td>
            </tr>
            </table>
            <![endif]-->
          </td>
        </tr>
        <!-- end copy block -->

        <!-- start footer -->
        <tr>
          <td align="center" bgcolor="#e9ecef" style="padding: 24px;">
            <!--[if (gte mso 9)|(IE)]>
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="600">
            <tr>
            <td align="center" valign="top" width="600">
            <![endif]-->
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px;">

              <!-- start permission -->
              <tr>
                <td align="center" bgcolor="#e9ecef" style="padding: 12px 24px; font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif; font-size: 14px; line-height: 20px; color: #666;">
                  <p style="margin: 0;">You received this email because we received a request for sign up for your account. If you didn't request it you can safely delete this email.</p>
                </td>
              </tr>
              <!-- end permission -->

            </table>
            <!--[if (gte mso 9)|(IE)]>
            </td>
            </tr>
            </table>
            <![endif]-->
          </td>
        </tr>
        <!-- end footer -->

      </table>
      <!-- end body -->

    </body>
    </html>
    ''' # noqa
