from datetime import datetime

import pytz

from common.constants.users import S3ClientConstants

S3Client_valid_response_date = datetime.strftime(
    datetime.utcnow().replace(
        tzinfo=pytz.timezone(S3ClientConstants.GMT_TIMEZONE.value),
    ),
    S3ClientConstants.AWS_S3_RESPONSE_DATETIME_FORMAT.value,
)

S3Client_upload_image_to_s3_valid_response = {
    'ResponseMetadata': {
        'RequestId': 'TJZ02NZG7YTNCP0E',
        'HostId': 'Ahv/BgjE/Ss1NE0w30I/gprmeHOL2GwPiLc636oOgeNLTglgP80Adxqz5CYZp+A5g9YdpCJOx1s=',
        'HTTPStatusCode': 200,
        'HTTPHeaders': {
            'x-amz-id-2': 'Ahv/BgjE/Ss1NE0w30I/gprmeHOL2GwPiLc636oOgeNLTglgP80Adxqz5CYZp+A5g9YdpCJOx1s=',
            'x-amz-request-id': 'TJZ02NZG7YTNCP0E',
            'date': S3Client_valid_response_date,
            'etag': '"1aa506098e25a0c499aa5e5ee94fa9e2"',
            'server': 'AmazonS3',
            'content-length': '0'
        },
        'RetryAttempts': 1
    },
    'ETag': '"70943e61f68653568ad8a3bf4390fbba"',
    'uploaded_file_url': 'https://dp-retraining-bucket.s3.eu-central-1.amazonaws.com/users/8b773a0c-455f-4953-b037-c9c1e83aea8d/profile_pics/5ac674b1-fd9b-4154-823f-fb337874daaf.png' # noqa
}
S3Client_delete_images_in_s3_valid_response = {
    'ResponseMetadata': {
        'RequestId': 'QGKFGPZQQZZWTRJ5',
        'HostId': 'omHged+Mgzk26CcZY6q0Z6JHGM+wnGQSmRBE+h1Iq+hWaozjPJiNVJiIWPOgUqbXWHDp3mC3PGzbm9gZCJpiFw==',
        'HTTPStatusCode': 204,
        'HTTPHeaders': {
            'x-amz-id-2': 'omHged+Mgzk26CcZY6q0Z6JHGM+wnGQSmRBE+h1Iq+hWaozjPJiNVJiIWPOgUqbXWHDp3mC3PGzbm9gZCJpiFw==',
            'x-amz-request-id': 'QGKFGPZQQZZWTRJ5',
            'date': S3Client_valid_response_date,
            'server': 'AmazonS3'
        },
        'RetryAttempts': 0
    }
}
