import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from common.constants.auth import EmailConfirmationTokenModelConstants
from db import Base


class EmailConfirmationToken(Base):
    """A model representing email confirmation token."""

    __tablename__ = 'email-confirmation-token'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    token = Column(String(EmailConfirmationTokenModelConstants.CHAR_SIZE_2048.value), nullable=True, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    expired_at = Column(DateTime, nullable=True)
    user = relationship('User', back_populates='email_confirmation_token', lazy='selectin')

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return (
            f'EmailConfirmationToken: id={self.id}, user_id={self.user_id}, token={self.token}, '
            f'expired_at={self.expired_at}'
        )
