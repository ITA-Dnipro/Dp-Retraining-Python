import enum


class UserModelConstants(enum.Enum):
    """User model constants."""
    # Numerics.
    CHAR_SIZE_64 = 64
    CHAR_SIZE_256 = 256
    CHAR_SIZE_512 = 512

    # Booleans.
    TRUE = True
    FALSE = False


class UserPictureModelConstants(enum.Enum):
    """User model constants."""
    # Numerics.
    CHAR_SIZE_512 = 512


class UserSchemaConstants(enum.Enum):
    """User schema constants."""
    # Numerics.
    CHAR_SIZE_2 = 2
    CHAR_SIZE_3 = 3
    CHAR_SIZE_6 = 6
    CHAR_SIZE_64 = 64
    CHAR_SIZE_256 = 256

    # Regex.
    EMAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class UserServiceConstants(enum.Enum):
    """User service constants."""
    IMAGE_SIZE_6_MB = 6_291_456
    FILE_JPG_EXTENSION = 'jpg'
    FILE_JPEG_EXTENSION = 'jpeg'
    FILE_PNG_EXTENSION = 'png'
    FILE_BMP_EXTENSION = 'bmp'
    FILE_GIF_EXTENSION = 'gif'
    VALID_IMAGE_EXTENSIONS = {
        FILE_JPG_EXTENSION: FILE_JPG_EXTENSION,
        FILE_JPEG_EXTENSION: FILE_JPEG_EXTENSION,
        FILE_PNG_EXTENSION: FILE_PNG_EXTENSION,
        FILE_BMP_EXTENSION: FILE_BMP_EXTENSION,
        FILE_GIF_EXTENSION: FILE_GIF_EXTENSION,
    }
    MIN_IMAGE_WIDTH = 32
    MAX_IMAGE_WIDTH = 5184
    MIN_IMAGE_HEIGHT = 32
    MAX_IMAGE_HEIGHT = 3456


class S3ClientConstants(enum.Enum):
    """S3 client constants."""
    S3_NAME = 's3'
    ACL_PUBLIC_READ = 'public-read'
    SUCCESSFUL_UPLOAD_MSG = 'File object uploaded to https://{bucket_name}.s3.{bucket_region}.amazonaws.com/{file_name}'
    PICTURE_FILE_NAME = 'users/{user_id}/profile_pics/{picture_id}.{file_extension}'
    CONTENT_TYPE_JPEG = 'image/jpeg'
    UPLOADED_FILE_URL = 'https://{bucket_name}.s3.{bucket_region}.amazonaws.com/{file_name}'
    AWS_S3_RESPONSE_DATETIME_FORMAT = '%a, %d %b %Y %H:%M:%S %Z'
    USER_PROFILE_PICS_FOLDER_NAME = (
        'users/{user_id}/profile_pics'
    )
    SUCCESSFUL_DELETE_MSG = 'File object successfully deleted {file_path}.'
    GMT_TIMEZONE = 'GMT'


class UserRouteConstants(enum.Enum):
    """User route constants."""
    ZERO_NUMBER = 0
    DEFAULT_START_PAGE = 1
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGINATION_PAGE_SIZE = 101
