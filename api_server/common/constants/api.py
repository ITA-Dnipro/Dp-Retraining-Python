import enum


@enum.unique
class ApiConstants(enum.Enum):
    """Project API versioning constants."""
    API_VERSION_V1 = 1
    LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s:%(lineno)s %(message)s'
