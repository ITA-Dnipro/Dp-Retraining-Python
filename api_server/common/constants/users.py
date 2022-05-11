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
    FILE_TIFF_EXTENSION = 'tiff'
    FILE_SVG_EXTENSION = 'svg'
    VALID_IMAGE_EXTENSIONS = {
        FILE_JPG_EXTENSION: FILE_JPG_EXTENSION,
        FILE_JPEG_EXTENSION: FILE_JPEG_EXTENSION,
        FILE_PNG_EXTENSION: FILE_PNG_EXTENSION,
        FILE_BMP_EXTENSION: FILE_BMP_EXTENSION,
        FILE_GIF_EXTENSION: FILE_GIF_EXTENSION,
        FILE_TIFF_EXTENSION: FILE_TIFF_EXTENSION,
        FILE_SVG_EXTENSION: FILE_SVG_EXTENSION,
    }
    MIN_IMAGE_WIDTH = 32
    MAX_IMAGE_WIDTH = 5184
    MIN_IMAGE_HEIGHT = 32
    MAX_IMAGE_HEIGHT = 3456


class S3HandlerConstants(enum.Enum):
    """S3 handler constants."""
    S3_NAME = 's3'
    ACL_PUBLIC_READ = 'public-read'
    SUCCESSFUL_UPLOAD_MSG = 'File object uploaded to https://{bucket_name}.s3.{bucket_region}.amazonaws.com/{file_name}'
    PICTURE_FILE_NAME = 'users/{user_id}/profile_pics/{user_id}.{file_extension}'
    CONTENT_TYPE_JPEG = 'image/jpeg'
