from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db import Base


class Employee(Base):
    """A model representing a employee."""

    __tablename__ = 'employees'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now())
    user = relationship('User', back_populates='employee', uselist=False, lazy='selectin')

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return f'Employee id={self.id}, user_id={self.user_id}, created_at={self.created_at}'
