import enum


@enum.unique
class CeleryConstants(enum.Enum):
    """Project Celery constants."""
    DEVELOPMENT_CONFIG = 'development'
    TESTING_CONFIG = 'testing'
