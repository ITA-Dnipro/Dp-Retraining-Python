import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from common.constants.fundraisers import FundraiseStatusModelConstants
from db import Base


class FundraiseStatusAssociation(Base):
    """Many-to-Many table for Fundraise and FundraiseStatus models association."""

    __tablename__ = 'fundraise_status_association'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    fundraise_id = Column(UUID(as_uuid=True), ForeignKey('fundraisers.id', ondelete='CASCADE'), nullable=False)
    status_id = Column(UUID(as_uuid=True), ForeignKey('fundraise_statuses.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    fundraise = relationship('Fundraise', back_populates='statuses', lazy='selectin')
    status = relationship('FundraiseStatus', back_populates='fundraisers', lazy='selectin')
    name = association_proxy('status', 'name')

    def __repr__(self):
        return (
            f'FundraiseStatusAssociation: fundraise_id={self.fundraise_id}, status_id={self.status_id}, '
            f'created_at={self.created_at}'
        )


class FundraiseStatus(Base):
    """A model representing a fundraise's status."""

    __tablename__ = 'fundraise_statuses'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(length=FundraiseStatusModelConstants.CHAR_SIZE_256.value), nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())

    fundraisers = relationship(
        'FundraiseStatusAssociation', back_populates='status', lazy='selectin',
    )

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return f'FundraiseStatus: id={self.id}, name={self.name}, created_at={self.created_at}'
