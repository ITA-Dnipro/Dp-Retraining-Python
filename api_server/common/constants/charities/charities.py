from enum import Enum


class CharitySchemaConstants(Enum):
    """Charities schema constants."""
    EMAIL_REGEX = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

    CHAR_SIZE_2 = 2
    CHAR_SIZE_128 = 128
    CHAR_SIZE_256 = 256
    CHAR_SIZE_512 = 512
    CHAR_SIZE_8192 = 8192


class CharityModelConstants(Enum):
    """Charities model constants."""
    CHAR_SIZE_128 = 128
    CHAR_SIZE_256 = 256
    CHAR_SIZE_512 = 512
    CHAR_SIZE_8192 = 8192


class CharityRouteConstants(Enum):
    """Charities route constants."""
    ZERO_NUMBER = 0
    DEFAULT_START_PAGE = 1
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGINATION_PAGE_SIZE = 101


class CharityEmployeeRoleConstants(Enum):
    """Charity EmployeeRole constants."""
    SUPERVISOR = 'supervisor'
    MANAGER = 'manager'

    EDIT_CHARITY_ROLES = (
        SUPERVISOR,
        MANAGER,
    )

    DELETE_CHARITY_ROLES = (
        SUPERVISOR,
    )
