from sqlalchemy.ext.asyncio import AsyncSession

from charities.models import Charity, CharityUserAssociation
from users.models import User
from utils.logging import setup_logging


class CharityEmployeeDBService:

    def __init__(self, session: AsyncSession) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def add_user_to_charity(self, user: User, charity: Charity) -> Charity:
        """Add User to Charity in the database via many-to-many relationship.

        Args:
            user: User object.
            charity: Charity object.

        Returns:
        Charity object with User added to many-to-many relationship.
        """
        return await self._add_user_to_charity(user, charity)

    async def _add_user_to_charity(self, user: User, charity: Charity) -> Charity:
        charity_user_association = CharityUserAssociation()
        charity_user_association.user = user
        charity_user_association.charity = charity
        self.session.add(charity_user_association)
        await self.session.commit()
        await self.session.refresh(charity_user_association)
        self._log.debug(
            f'User with id: "{user.id}" added to Charity with id: {charity.id}.'
        )
        return charity
