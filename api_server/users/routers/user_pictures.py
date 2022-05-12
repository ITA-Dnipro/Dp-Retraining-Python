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
