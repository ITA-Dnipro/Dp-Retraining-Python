import enum


class SqlalchemyExceptionConstants(enum.Enum):
    """sqlalchemy exceptions constants."""
    INTEGRITY_ERROR_TABLE_NAME_REGEX = r'"(.*?)"'
    INTEGRITY_ERROR_FIELD_VALUE_REGEX = r'\((.*?)\)'
