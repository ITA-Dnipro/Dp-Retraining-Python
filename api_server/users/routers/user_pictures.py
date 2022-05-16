from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, status

from common.schemas.responses import ResponseBaseSchema
from users.schemas.user_pictures import UserPictureOutputSchema
from users.services.user_pictures import UserPictureService

user_pictures_router = APIRouter(prefix='/pictures', tags=['User-pictures'])


@user_pictures_router.post('/', response_model=ResponseBaseSchema, status_code=status.HTTP_201_CREATED)
async def post_user_pictures(
        user_id: UUID,
        image: UploadFile,
        user_picture_service: UserPictureService = Depends(),
):
    """POST '/users/{user_id}/pictures' endpoint view function.

    Args:
        user_id: UUID of a User.
        image: image: Uploaded user image.
        user_picture_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with UserPictureOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_201_CREATED,
        data=UserPictureOutputSchema.from_orm(await user_picture_service.add_user_picture(id_=user_id, image=image)),
        errors=[],
    )


@user_pictures_router.put('/{picture_id}', response_model=ResponseBaseSchema)
async def put_user_picture(
        user_id: UUID,
        picture_id: UUID,
        image: UploadFile,
        user_picture_service: UserPictureService = Depends(),
):
    """PUT '/users/{user_id}/pictures/{picture_id}' endpoint view function.

    Args:
        user_id: UUID of a User object.
        picture_id: UUID of a UserPicture object.
        image: image: Uploaded user image.
        user_picture_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with UserPictureOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=UserPictureOutputSchema.from_orm(await user_picture_service.update_user_picture(
            id_=user_id, picture_id=picture_id, image=image,
        )),
        errors=[],
    )
