import enum


class FundraiseStatusModelConstants(enum.Enum):
    """FundraiseStatus model constants."""
    CHAR_SIZE_256 = 256


class FundraiseStatusSchemaConstants(enum.Enum):
    """FundraiseStatus schema constants."""
    CHAR_SIZE_2 = 2
    CHAR_SIZE_256 = 256


class FundraiseStatusConstants(enum.Enum):
    """FundraiseStatus constants."""
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

    ADD_STATUS_MAPPING = {
        NEW: (None,),
        IN_PROGRESS: (NEW, ON_HOLD, COMPLETED),
        ON_HOLD: (NEW, IN_PROGRESS, COMPLETED),
        COMPLETED: (NEW, IN_PROGRESS, ON_HOLD),
    }

    FUNDRAISE_IS_DONATABLE_STATUS_MAPPING = {
        NEW: True,
        IN_PROGRESS: True,
        ON_HOLD: False,
        COMPLETED: False,
    }
