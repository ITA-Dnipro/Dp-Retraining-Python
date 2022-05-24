from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from db import Base


class CharityUserAssociation(Base):
    """Many-to-Many table for CharityOrganisation and User models association."""

    __tablename__ = 'charity_user_association'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)

    charity_id = Column(UUID(as_uuid=True), ForeignKey('CharityOrganisations.id'), nullable=False)
    users_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    charity = relationship('CharityOrganisation', back_populates='users_association', lazy="selectin")
    user = relationship('User', back_populates='charities', lazy="selectin")

    def __repr__(self):
        return "Auxiliary table that connects CharityOrganisation and Users"


class CharityOrganisation(Base):
    __tablename__ = "CharityOrganisations"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String(250))
    organisation_email = Column(String(120))
    phone_number = Column(String(15))
    created_at = Column(DateTime, default=datetime.now())

    users_association = relationship('CharityUserAssociation', back_populates='charity', lazy="selectin")
    users = association_proxy('users_association', 'user')

    def __repr__(self):
        return f"Organisation {self.title}. Contact phone: {self.phone_number} and email: {self.organisation_email}"
