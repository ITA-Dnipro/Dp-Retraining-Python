from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from common.constants.charities import CharityModelConstants
from db import Base


class CharityUserAssociation(Base):
    """Many-to-Many table for Charity and User models association."""

    __tablename__ = 'charity_user_association'
    __table_args__ = (
        UniqueConstraint('charity_id', 'user_id', name='_charity_user_uc'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    charity_id = Column(UUID(as_uuid=True), ForeignKey('charities.id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    charity = relationship('Charity', back_populates='users_association', lazy='selectin')
    user = relationship('User', back_populates='charities', lazy='selectin')

    def __repr__(self):
        return f'CharityUserAssociation: charity_id={self.charity_id}, user_id={self.users_id}, created_at={self.created_at}' # noqa


class Charity(Base):
    """A model representing a charity."""

    __tablename__ = 'charities'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String(length=CharityModelConstants.CHAR_SIZE_512.value), unique=True)
    description = Column(String(length=CharityModelConstants.CHAR_SIZE_8192.value))
    email = Column(String(length=CharityModelConstants.CHAR_SIZE_256.value), unique=True)
    phone_number = Column(String(length=CharityModelConstants.CHAR_SIZE_128.value), unique=True)
    created_at = Column(DateTime, default=datetime.now())

    users_association = relationship(
        'CharityUserAssociation', back_populates='charity', lazy='selectin', cascade='all, delete',
    )
    users = association_proxy('users_association', 'user')

    fundraisers = relationship('Fundraise', back_populates='charity', lazy='selectin', cascade='all, delete')

    def __repr__(self):
        return f'Charity id={self.id}, title={self.title}, created_at={self.created_at}'
