from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from common.constants.charities import EmployeeRoleModelConstants
from db import Base


class EmployeeRole(Base):
    """A model representing a employee role."""

    __tablename__ = 'employee_roles'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(length=EmployeeRoleModelConstants.CHAR_SIZE_256.value), unique=True)
    created_at = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f'EmployeeRole id={self.id}, name={self.name}, created_at={self.created_at}'
