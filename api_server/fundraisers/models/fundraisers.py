import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from common.constants.fundraisers import FundraiseModelConstants
from db import Base


class Fundraise(Base):
    """A model representing a fundraise."""

    __tablename__ = 'fundraisers'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    charity_id = Column(UUID(as_uuid=True), ForeignKey('charities.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(length=FundraiseModelConstants.CHAR_SIZE_512.value), nullable=False)
    description = Column(String(length=FundraiseModelConstants.CHAR_SIZE_8192.value), nullable=False)
    goal = Column(
        Numeric(
            precision=FundraiseModelConstants.NUM_PRECISION.value,
            scale=FundraiseModelConstants.NUM_SCALE.value,
        ),
        nullable=False,
    )
    created_at = Column(DateTime, server_default=func.now())
    ending_at = Column(DateTime, nullable=True)
    is_donatable = Column(Boolean, nullable=False, default=True)

    charity = relationship(
        'Charity', back_populates='fundraisers', uselist=False, lazy='selectin',
    )
    statuses = relationship(
        'FundraiseStatusAssociation', back_populates='fundraise', lazy='selectin', cascade='all, delete',
    )

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return f'Fundraise: title={self.title}, goal={self.goal}, ending_at={self.ending_at}'
