import enum


class FundraiseStatusPopulateData(enum.Enum):
    """FundraiseStatus table population data."""
    NEW = 'New'
    IN_PROGRESS = 'In progress'
    ON_HOLD = 'On hold'
    COMPLETED = 'Completed'
    ALL_STATUSES = [
        NEW,
        IN_PROGRESS,
        ON_HOLD,
        COMPLETED,
    ]
