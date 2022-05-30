from uuid import UUID
import abc

from fastapi import Depends

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from auth.cruds import EmailConfirmationTokenCRUD
from auth.tasks import send_email_comfirmation_letter
from auth.utils.jwt_tokens import create_jwt_token, create_token_payload
from common.constants.auth.email_confirmation_tokens import EmailConfirmationTokenConstants
from db import get_session
from users.cruds import UserCRUD
from users.models import User
from users.schemas import UserInputSchema, UserUpdateSchema
from users.utils.jwt.user import jwt_user_validator
from users.utils.pagination import PaginationPage
from utils.logging import setup_logging


class AbstractUserService(metaclass=abc.ABCMeta):

    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        Authorize: AuthJWT = Depends(),
    ) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session
        self.Authorize = Authorize
        self.user_crud = UserCRUD(session=self.session)
        self.email_confirmation_token_crud = EmailConfirmationTokenCRUD(session=self.session)

    async def get_users(self, page: int, page_size: int) -> list[User]:
        """Get User objects from database.

        Args:
            page: number of result page.
            page_size: number of items per page.

        Returns:
        list of User objects.
        """
        return await self._get_users(page, page_size)

    async def get_user_by_id(self, id_: UUID) -> User:
        """Get User object from database filtered by id.

        Args:
            id_: UUID of user.

        Returns:
        single User object filtered by id.
        """
        return await self._get_user_by_id(id_)

    async def add_user(self, user: UserInputSchema) -> User:
        """Add User object to the database.

        Args:
            user: UserInputSchema object.

        Returns:
        newly created User object.
        """
        return await self._add_user(user)

    async def update_user(self, id_: UUID, user: UserUpdateSchema) -> User:
        """Updates User object in the database.

        Args:
            id_: UUID of user.
            user: UserUpdateSchema object.

        Returns:
        updated User object.
        """
        return await self._update_user(id_, user)

    async def delete_user(self, id_: UUID) -> None:
        """Delete User object from the database.

        Args:
            id_: UUID of user.

        Returns:
        Nothing.
        """
        return await self._delete_user(id_)

    async def get_user_by_username(self, username: str) -> User:
        """Get User object from database filtered by username.

        Args:
            username: string of User's username.

        Returns:
        Single User object filtered by username.
        """
        return await self._get_user_by_username(username)

    @abc.abstractclassmethod
    async def _get_users(self, page: int, page_size: int) -> None:
        pass

    @abc.abstractclassmethod
    async def _get_user_by_id(self, id_: UUID) -> None:
        pass

    @abc.abstractclassmethod
    async def _add_user(self, user: UserInputSchema) -> None:
        pass

    @abc.abstractclassmethod
    async def _update_user(self, id_: UUID, user: UserUpdateSchema) -> None:
        pass

    @abc.abstractclassmethod
    async def _delete_user(self, id_: UUID) -> None:
        pass

    @abc.abstractclassmethod
    async def _get_user_by_username(self, username: str) -> None:
        pass


class UserService(AbstractUserService):

    async def _get_users(self, page: int, page_size: int) -> None:
        users = await self.user_crud._get_users(page, page_size)
        total_users = await self.user_crud._get_total_of_users()
        return PaginationPage(items=users, page=page, page_size=page_size, total=total_users)

    async def _get_user_by_id(self, id_: str) -> None:
        return await self.user_crud._get_user_by_id(id_)

    async def _add_user(self, user: UserInputSchema) -> User:
        user = await self.user_crud._add_user(user)
        # Creating EmailConfirmationToken.
        jwt_token_payload = create_token_payload(
            data=str(user.id),
            time_amount=EmailConfirmationTokenConstants.TOKEN_EXPIRE_7.value,
            time_unit=EmailConfirmationTokenConstants.MINUTES.value,
        )
        jwt_token = create_jwt_token(payload=jwt_token_payload, key=user.password)
        db_email_confirmation_token = await self.email_confirmation_token_crud.add_email_confirmation_token(
            id_=user.id,
            token=jwt_token,
        )
        # Start of the sending confirmation email task.
        send_email_comfirmation_letter.apply_async(
            kwargs={
                'email_confirmation_token': db_email_confirmation_token,
            },
            serializers='pickle',
        )
        return user

    async def _update_user(self, id_: str, user: UserUpdateSchema) -> None:
        self.Authorize.jwt_required()
        jwt_subject = self.Authorize.get_jwt_subject()
        user_exists = await self.user_crud._select_user(column='id', value=id_)
        if user_exists:
            if jwt_user_validator(jwt_subject=jwt_subject, username=user_exists.username):
                # Updating user.
                return await self.user_crud.update_user(id_, user)

    async def _delete_user(self, id_) -> None:
        self.Authorize.jwt_required()
        jwt_subject = self.Authorize.get_jwt_subject()
        user_exists = await self.user_crud._select_user(column='id', value=id_)
        if user_exists:
            if jwt_user_validator(jwt_subject=jwt_subject, username=user_exists.username):
                # Deleting user.
                return await self.user_crud.delete_user(id_)

    async def _get_user_by_username(self, username: str) -> None:
        return await self.user_crud._select_user(column='username', value=username)
