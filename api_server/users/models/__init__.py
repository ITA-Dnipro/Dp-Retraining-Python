import uuid

from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from common.constants.users import UserModelConstants

Base = declarative_base()


class User(Base):
    """A model representing a user."""

    __tablename__ = "Users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=True)
    last_name = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=True)
    username = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=False)
    email = Column(String(UserModelConstants.CHAR_SIZE_256.value), nullable=False)
    password = Column(String(UserModelConstants.CHAR_SIZE_256.value), nullable=True)
    phone_number = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=False)
    is_active = Column(Boolean, nullable=True, default=UserModelConstants.FALSE.value)
    created_at = Column(DateTime, server_default=func.now())

    __mapper_args__ = {"eager_defaults": True}
