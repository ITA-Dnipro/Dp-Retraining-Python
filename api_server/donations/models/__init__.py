import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, func
from sqlalchemy.dialects.postgresql import UUID

from db import Base


class Donation(Base):
    """A model representing a donation."""

    __tablename__ = "Donations"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey('Balances.id'), default=uuid.uuid4)
    recipient_id = Column(UUID(as_uuid=True), ForeignKey('Balances.id'), default=uuid.uuid4)
    amount = Column(Numeric(precision=4, scale=2), default=0)
    created_at = Column(DateTime, server_default=func.now())
    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f'Balance: {self.amount}₴'