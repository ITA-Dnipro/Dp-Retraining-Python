from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from common.schemas.responses import ResponseBaseSchema
from users.routers.user_pictures import user_pictures_router
from users.schemas import UserInputSchema, UserOutputSchema, UserUpdateSchema
from users.services import UserService

users_router = APIRouter(prefix='/users', tags=['Users'])
users_router.include_router(user_pictures_router, prefix='/{user_id}')


@users_router.get('/', response_model=ResponseBaseSchema)
async def get_users(user_service: UserService = Depends()) -> ResponseBaseSchema:
    """GET '/users' endpoint view function.

    Args:
        user_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with list of UserOutputSchema objects as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=[UserOutputSchema.from_orm(user) for user in await user_service.get_users()],
        errors=[],
    )


@users_router.get('/{id}', response_model=ResponseBaseSchema)
async def get_user(id: UUID, user_service: UserService = Depends()) -> ResponseBaseSchema:
    """GET '/users/{id}' endpoint view function.

    Args:
        id: UUID of user.
        user_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with UserOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=UserOutputSchema.from_orm(await user_service.get_user_by_id(id_=id)),
        errors=[],
    )


@users_router.post('/', response_model=ResponseBaseSchema, status_code=status.HTTP_201_CREATED)
async def post_users(
        user: UserInputSchema,
        user_service: UserService = Depends(),
) -> ResponseBaseSchema:
    """POST '/users' endpoint view function.

    Args:
        user: Serialized UserInputSchema object.
        user_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with UserOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_201_CREATED,
        data=UserOutputSchema.from_orm(await user_service.add_user(user=user)),
        errors=[],
    )


@users_router.put('/{id}', response_model=ResponseBaseSchema)
async def put_user(id: UUID, user: UserUpdateSchema, user_service: UserService = Depends()) -> ResponseBaseSchema:
    """PUT '/users/{id}' endpoint view function.

    Args:
        id: UUID of user.
        user: Serialized UserUpdateSchema object.
        user_service: dependency as business logic instance.

    Returns:
    ResponseBaseSchema object with UserOutputSchema object as response data.
    """
    return ResponseBaseSchema(
        status_code=status.HTTP_200_OK,
        data=UserOutputSchema.from_orm(await user_service.update_user(id_=id, user=user)),
        errors=[],
    )


@users_router.delete('/{id}')
async def delete_user(id: UUID, user_service: UserService = Depends()) -> Response:
    """DELETE '/users/{id}' endpoint view function.

    Args:
        id: UUID of user.
        user_service: dependency as business logic instance.

    Returns:
    http response with no data and 204 status code.
    """
    await user_service.delete_user(id_=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
