import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from common.constants.auth import ChangePasswordTokenModelConstants
from db import Base


class ChangePasswordToken(Base):
    """A model representing change password token."""

    __tablename__ = 'change-password-token'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('Users.id'), nullable=False)
    token = Column(String(ChangePasswordTokenModelConstants.CHAR_SIZE_2048.value), nullable=True, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    expired_at = Column(DateTime, nullable=True)
    user = relationship('User', back_populates='change_password_token', lazy='selectin')

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return (
            f'ChangePasswordToken: id={self.id}, user_id={self.user_id}, token={self.token}, '
            f'expired_at={self.expired_at}'
        )
