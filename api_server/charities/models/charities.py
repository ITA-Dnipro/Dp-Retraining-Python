from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from common.constants.charities.charities import CharityModelConstants
from db import Base


class CharityEmployeeRoleAssociation(Base):
    """Many-to-Many table for CharityEmployeeAssociation and EmployeeRole models association."""

    __tablename__ = 'charity_employee_role_association'
    __table_args__ = (
        UniqueConstraint('charity_employee_id', 'role_id', name='_charity_employee_role_uc'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    charity_employee_id = Column(UUID(as_uuid=True), ForeignKey('charity_employee_association.id'), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey('employee_roles.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return (
            f'CharityEmployeeRoleAssociation: charity_employee_id={self.charity_employee_id}, '
            f'role_id={self.role_id}, created_at={self.created_at}'
        )


class CharityEmployeeAssociation(Base):
    """Many-to-Many table for Charity and Employee models association."""

    __tablename__ = 'charity_employee_association'
    __table_args__ = (
        UniqueConstraint('charity_id', 'employee_id', name='_charity_employee_uc'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    charity_id = Column(UUID(as_uuid=True), ForeignKey('charities.id'), nullable=False)
    employee_id = Column(UUID(as_uuid=True), ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    roles = relationship(
        'EmployeeRole',
        secondary='charity_employee_role_association',
        lazy='subquery',
    )

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return (
            f'CharityUserAssociation: charity_id={self.charity_id}, employee_id={self.employee_id}, '
            f'created_at={self.created_at}'
        )


class Charity(Base):
    """A model representing a charity."""

    __tablename__ = 'charities'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String(length=CharityModelConstants.CHAR_SIZE_512.value), unique=True)
    description = Column(String(length=CharityModelConstants.CHAR_SIZE_8192.value))
    email = Column(String(length=CharityModelConstants.CHAR_SIZE_256.value), unique=True)
    phone_number = Column(String(length=CharityModelConstants.CHAR_SIZE_128.value), unique=True)
    created_at = Column(DateTime, default=datetime.now())

    employees = relationship('Employee', secondary='charity_employee_association', lazy='subquery')

    fundraisers = relationship('Fundraise', back_populates='charity', lazy='selectin', cascade='all, delete')

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return f'Charity id={self.id}, title={self.title}, created_at={self.created_at}'
