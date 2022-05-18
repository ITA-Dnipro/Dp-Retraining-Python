import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from common.constants.users import UserModelConstants, UserPictureModelConstants
from db import Base


class User(Base):
    """A model representing a user."""

    __tablename__ = 'Users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=True)
    last_name = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=True)
    username = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=False, unique=True)
    email = Column(String(UserModelConstants.CHAR_SIZE_256.value), nullable=False, unique=True)
    password = Column(String(UserModelConstants.CHAR_SIZE_256.value), nullable=True)
    phone_number = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=False, unique=True)
    activated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    profile_picture = relationship(
        'UserPicture', back_populates='user', uselist=False, lazy='selectin', cascade='all, delete',
    )
    email_confirmation_token = relationship(
        'EmailConfirmationToken', back_populates='user', uselist=False, lazy='selectin', cascade='all, delete',
    )

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return f'User: id={self.id}, username={self.username}, email={self.email}'


class UserPicture(Base):
    """A model representing user's profile picture."""

    __tablename__ = 'user-pictures'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False, unique=True)
    url = Column(String(UserPictureModelConstants.CHAR_SIZE_512.value), nullable=True, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)
    user = relationship('User', back_populates='profile_picture')
    etag = Column(String(UserPictureModelConstants.CHAR_SIZE_512.value), nullable=True)

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return f'UserPicture: id={self.id}, url={self.url}, created_at={self.created_at}'
