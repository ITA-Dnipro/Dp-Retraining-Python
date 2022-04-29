import enum


@enum.unique
class ApiVersion(enum.Enum):
    """Project API versioning constants."""
    V1 = 1
