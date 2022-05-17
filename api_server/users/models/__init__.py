import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID

from common.constants.users import UserModelConstants
from db import Base


class User(Base):
    """A model representing a user."""

    __tablename__ = "Users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    first_name = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=True)
    last_name = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=True)
    username = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=False, unique=True)
    email = Column(String(UserModelConstants.CHAR_SIZE_256.value), nullable=False, unique=True)
    password = Column(String(UserModelConstants.CHAR_SIZE_256.value), nullable=True)
    phone_number = Column(String(UserModelConstants.CHAR_SIZE_64.value), nullable=False, unique=True)
    is_active = Column(Boolean, nullable=True, default=UserModelConstants.FALSE.value)
    created_at = Column(DateTime, server_default=func.now())
    balance_id = Column(UUID(as_uuid=True), ForeignKey('Balances.id'), default=uuid.uuid4)
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f'User: id={self.id}, username={self.username}, email={self.email}'
