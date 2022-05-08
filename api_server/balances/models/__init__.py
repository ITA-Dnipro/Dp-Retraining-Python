import uuid

from sqlalchemy import Column, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Balance(Base):
    """A model representing a balance."""

    __tablename__ = "Balance"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    amount = Column(Numeric(precision=2), default=0)

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f'Balance: {self.amount}₴'
