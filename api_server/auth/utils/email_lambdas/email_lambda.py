import html
import json

import boto3


def send_email(event, context):
    """Sends email letter to the recipient.

    Args:
        event: AWS lambda event.
        context: AWS lambda context.

    Returns:
    Response object from boto3 ses client.
    """
    return _send_email(event, context)


def _send_email(event, context):
    email_data = get_email_data(event)

    client = boto3.client('ses')

    response = client.send_email(
        Source=email_data['source'],
        Destination={'ToAddresses': [email_data['to_address']]},
        Message={
            'Body': {
                'Html': {
                    'Charset': email_data['charset'],
                    'Data': email_data['html'],
                },
            },
            'Subject': {
                'Charset': email_data['charset'],
                'Data': email_data['subject'],
            },
        },
    )
    return response


def get_email_data(event) -> dict:
    """Loads incoming json data to compose email letter data.

    Args:
        event: AWS lambda event.

    Returns:
    dict with email letter data.
    """
    payload = json.loads(event['body'])
    payload['html'] = html.unescape(payload['html'])
    return payload


def lambda_handler(event, context):
    """Email sending main handler function.

    Args:
        event: AWS lambda event.
        context: AWS lambda context.

    Returns:
    Response object from boto3 ses client.
    """
    return send_email(event, context)
