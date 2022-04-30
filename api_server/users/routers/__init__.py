from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from users.schemas import UserInputSchema, UserOutputSchema
from users.services import UserService

users_router = APIRouter(prefix='/users', tags=['Users'])


@users_router.get('/', response_model=list[UserOutputSchema])
async def get_users(session: AsyncSession = Depends(get_session)):
    """GET '/users' endpoint func, return list of User objects."""
    return await UserService(session=session).get_users()


@users_router.get('/{id}', response_model=UserOutputSchema)
async def get_user(id: UUID, session: AsyncSession = Depends(get_session)):
    """GET '/users/{id}' endpoint func, return single User object."""
    return await UserService(session=session).get_user_by_id(id_=id)


@users_router.post('/', response_model=UserOutputSchema)
async def post_users(user: UserInputSchema, session: AsyncSession = Depends(get_session)):
    """POST '/users' endpoint func, create and return a single User object."""
    return await UserService(session=session).add_user(user=user)


@users_router.put('/{id}', response_model=UserOutputSchema)
async def put_user(id: UUID, user: UserInputSchema, session: AsyncSession = Depends(get_session)):
    """PUT '/users/{id}' endpoint func, update and return a single User object."""
    return await UserService(session=session).update_user(id_=id, user=user)


@users_router.delete('/{id}')
async def delete_user(id: UUID, session: AsyncSession = Depends(get_session)):
    """DELETE '/users/{id}' endpoint func, deletes a single User object."""
    await UserService(session=session).delete_user(id_=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
