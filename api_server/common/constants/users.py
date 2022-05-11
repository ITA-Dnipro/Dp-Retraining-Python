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


class S3HandlerConstants(enum.Enum):
    """S3 handler constants."""
    S3_NAME = 's3'
    ACL_PUBLIC_READ = 'public-read'
    SUCCESSFUL_UPLOAD_MSG = 'File object uploaded to https://{bucket_name}.s3.{bucket_region}.amazonaws.com/{file_name}'
    PICTURE_FILE_NAME = 'users/{user_id}/profile_pics/{user_id}.{file_extension}'
    CONTENT_TYPE_JPEG = 'image/jpeg'
