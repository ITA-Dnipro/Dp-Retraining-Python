import enum


class FundraiseRouteConstants(enum.Enum):
    """Fundraise route constants."""
    ZERO_NUMBER = 0
    DEFAULT_START_PAGE = 1
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGINATION_PAGE_SIZE = 101


class FundraiseModelConstants(enum.Enum):
    """Fundraise model constants."""
    # Numerics.
    CHAR_SIZE_64 = 64
    CHAR_SIZE_256 = 256
    CHAR_SIZE_512 = 512
    CHAR_SIZE_8192 = 8192

    NUM_PRECISION = 20
    NUM_SCALE = 2


class FundraiseSchemaConstants(enum.Enum):
    """Fundraise schema constants."""
    # Numerics.
    CHAR_SIZE_2 = 2
    CHAR_SIZE_512 = 512
    CHAR_SIZE_8192 = 8192

    MIN_VALUE = 0
    NUM_PRECISION = 20
    NUM_SCALE = 2


class FundraiseStatusModelConstants(enum.Enum):
    """FundraiseStatus model constants."""
    CHAR_SIZE_256 = 256


class FundraiseStatusSchemaConstants(enum.Enum):
    """FundraiseStatus schema constants."""
    CHAR_SIZE_2 = 2
    CHAR_SIZE_256 = 256
