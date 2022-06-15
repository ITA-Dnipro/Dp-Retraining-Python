import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from common.constants.fundraisers import FundraiseModelConstants
from db import Base


class Fundraise(Base):
    """A model representing a fundraise."""

    __tablename__ = 'fundraisers'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    charity_id = Column(UUID(as_uuid=True), ForeignKey('CharityOrganisations.id'), nullable=False)
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

    charity = relationship(
        'CharityOrganisation', back_populates='fundraisers', uselist=False, lazy='selectin',
    )
    statuses_association = relationship(
        'FundraiseStatusAssociation', back_populates='fundraise', lazy='selectin',
    )
    statuses = association_proxy('statuses_association', 'status')

    __mapper_args__ = {'eager_defaults': True}

    def __repr__(self):
        return f'Fundraise: title={self.title}, goal={self.goal}, ending_at={self.ending_at}'
