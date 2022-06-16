from sqlalchemy.ext.asyncio import AsyncSession

from charities.models import CharityOrganisation, CharityUserAssociation
from users.models import User
from utils.logging import setup_logging


class CharityEmployeeDBService:

    def __init__(self, session: AsyncSession) -> None:
        self._log = setup_logging(self.__class__.__name__)
        self.session = session

    async def add_user_to_charity(self, user: User, charity: CharityOrganisation) -> CharityOrganisation:
        """Add User to CharityOrganisation in the database via many-to-many relationship.

        Args:
            user: User object.
            charity: CharityOrganisation object.

        Returns:
        CharityOrganisation object with User added to many-to-many relationship.
        """
        return await self._add_user_to_charity(user, charity)

    async def _add_user_to_charity(self, user: User, charity: CharityOrganisation) -> CharityOrganisation:
        charity_user_association = CharityUserAssociation()
        charity_user_association.user = user
        charity_user_association.charity = charity
        self.session.add(charity_user_association)
        await self.session.commit()
        await self.session.refresh(charity_user_association)
        self._log.debug(
            f'User with id: "{user.id}" added to CharityOrganisation with id: {charity.id}.'
        )
        return charity
