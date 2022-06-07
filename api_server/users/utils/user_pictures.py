from fastapi import UploadFile, status

from PIL import Image

from common.constants.users import UserServiceConstants
from common.exceptions.users import UserPictureExceptionMsgs
from users.utils.exceptions import UserPictureExtensionError, UserPictureResolutionError, UserPictureSizeError


class UserProfileImageValidator:

    @staticmethod
    async def validate_image(image: UploadFile) -> None:
        """Validates image size, extension and resolution raises exceptions in case of invalidation.

        Args:
            image: UploadFile image object.

        Raise:
            UserPictureSizeError if image size exceeds maximum image size.
            UserPictureExtensionError if image extension not supported.
            UserPictureResolutionError if image resolution not in allowed image resolution range.

        Returns:
            Nothing.
        """
        await UserProfileImageValidator.validate_image_size(image)
        await UserProfileImageValidator.validate_image_extension(image)
        await UserProfileImageValidator.validate_image_resolution(image)

    @staticmethod
    async def validate_image_size(image: UploadFile) -> None:
        """Validates image size and raises exception in case of invalidation.

        Args:
            image: UploadFile image object.

        Raise:
            UserPictureSizeError if image size exceeds maximum image size.

        Returns:
        Nothing.
        """
        if await UserProfileImageValidator._validate_image_size(image):
            raise UserPictureSizeError(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=UserPictureExceptionMsgs.IMAGE_EXCEED_MAX_SIZE.value,
            )

    @staticmethod
    async def _validate_image_size(image: UploadFile) -> bool:
        """Checks currently uploaded image size to the maximum image size threshold.

        Args:
            image: UploadFile image object.

        Returns:
        bool of comparison uploaded image size and maximum image size threshold.
        """
        image_size = len(await image.read())
        return image_size >= UserServiceConstants.IMAGE_SIZE_6_MB.value

    @staticmethod
    async def validate_image_extension(image: UploadFile) -> None:
        """Validates image extension and raises exception in case of invalidation.

        Args:
            image: UploadFile image object.

        Raise:
            UserPictureExtensionError if image extension not supported.

        Returns:
        Nothing.
        """
        if not await UserProfileImageValidator._validate_image_extension(image):
            raise UserPictureExtensionError(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=UserPictureExceptionMsgs.UNSUPPORTED_IMAGE_EXTENSION.value,
            )

    @staticmethod
    async def _validate_image_extension(image: UploadFile) -> bool:
        """Checks if currently uploaded image's exception present in mapping of allowed image file extensions.

        Args:
            image: UploadFile image object.

        Returns:
        bool of presence uploaded image's extension in allowed image file extensions.
        """
        image_extension = image.filename.split('.')[-1].lower()
        return bool(UserServiceConstants.VALID_IMAGE_EXTENSIONS.value.get(image_extension))

    @staticmethod
    async def validate_image_resolution(image: UploadFile) -> None:
        """Validates image resolution in allowed range and raises exception in case of invalidation.

        Args:
            image: UploadFile image object.

        Raise:
            UserPictureResolutionError if image resolution not in allowed image resolution range.

        Returns:
        Nothing.
        """
        if not await UserProfileImageValidator._validate_image_resolution(image):
            raise UserPictureResolutionError(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=UserPictureExceptionMsgs.INVALID_IMAGE_RESOLUTION.value,
            )

    @staticmethod
    async def _validate_image_resolution(image: UploadFile) -> bool:
        """Checks if currently uploaded image's width and height present in allowed image resolution range.

        Args:
            image: UploadFile image object.

        Returns:
        bool of presence uploaded image's width and height in allowed image resolution range.
        """
        pillow_image = Image.open(image.file)
        width_check = pillow_image.width in range(
            UserServiceConstants.MIN_IMAGE_WIDTH.value,
            UserServiceConstants.MAX_IMAGE_WIDTH.value,
        )
        height_check = pillow_image.height in range(
            UserServiceConstants.MIN_IMAGE_HEIGHT.value,
            UserServiceConstants.MAX_IMAGE_HEIGHT.value,
        )
        return width_check and height_check
