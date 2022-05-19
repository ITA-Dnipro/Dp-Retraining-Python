import os

from dotenv import load_dotenv
from pydantic import BaseModel

from common.constants.api import ApiConstants
from common.constants.celery import CeleryConstants

load_dotenv()


class DevelopmentConfig(BaseModel):
    """Stores all project settings."""

    # App settings.
    API_SERVER_HOST: str = os.getenv('API_SERVER_HOST')
    API_SERVER_PORT: int = int(os.getenv('API_SERVER_PORT'))
    API_SERVER_LOG_LEVEL: str = os.getenv('API_SERVER_LOG_LEVEL')
    API_SERVER_RELOAD: bool = (os.getenv('API_SERVER_RELOAD', 'False') == 'True')
    API_SQLALCHEMY_ECHO: bool = (os.getenv('API_SQLALCHEMY_ECHO', 'False') == 'True')
    API_SQLALCHEMY_FUTURE: bool = (os.getenv('API_SQLALCHEMY_FUTURE', 'False') == 'True')

    # Postgres settings.
    POSTGRES_DIALECT_DRIVER: str = os.getenv('POSTGRES_DIALECT_DRIVER')
    POSTGRES_DB_USERNAME: str = os.getenv('POSTGRES_DB_USERNAME')
    POSTGRES_DB_PASSWORD: str = os.getenv('POSTGRES_DB_PASSWORD')
    POSTGRES_DB_HOST: str = os.getenv('POSTGRES_DB_HOST')
    POSTGRES_DB_PORT: str = os.getenv('POSTGRES_DB_PORT')
    POSTGRES_DB_NAME: str = os.getenv('POSTGRES_DB_NAME')
    POSTGRES_DATABASE_URL = (
        f'{POSTGRES_DIALECT_DRIVER}://{POSTGRES_DB_USERNAME}:'
        f'{POSTGRES_DB_PASSWORD}@{POSTGRES_DB_HOST}:'
        f'{POSTGRES_DB_PORT}/{POSTGRES_DB_NAME}'
    )

    # JWT settings.
    authjwt_secret_key: str = os.getenv('authjwt_secret_key')
    authjwt_token_location: set = {os.getenv('authjwt_token_location')}
    authjwt_cookie_csrf_protect: bool = (os.getenv('authjwt_cookie_csrf_protect', 'False') == 'True')


class TestingConfig(BaseModel):
    """Testing configuration variables for the project."""
    # App settings.
    API_SERVER_HOST: str = os.getenv('API_SERVER_HOST')
    API_SERVER_PORT: int = int(os.getenv('API_SERVER_PORT'))
    API_SERVER_LOG_LEVEL: str = os.getenv('API_SERVER_LOG_LEVEL')
    API_SERVER_RELOAD: bool = (os.getenv('API_SERVER_RELOAD', 'False') == 'True')
    API_SQLALCHEMY_ECHO: bool = (os.getenv('API_SQLALCHEMY_ECHO', 'False') == 'True')
    API_SQLALCHEMY_FUTURE: bool = (os.getenv('API_SQLALCHEMY_FUTURE', 'False') == 'True')

    # Postgres settings.
    POSTGRES_DIALECT_DRIVER: str = os.getenv('POSTGRES_DIALECT_DRIVER')
    POSTGRES_DB_USERNAME: str = os.getenv('POSTGRES_DB_USERNAME')
    POSTGRES_DB_PASSWORD: str = os.getenv('POSTGRES_DB_PASSWORD')
    POSTGRES_DB_HOST: str = os.getenv('POSTGRES_DB_HOST')
    POSTGRES_DB_PORT: str = os.getenv('POSTGRES_DB_PORT')
    POSTGRES_DB_NAME: str = 'test_postgres'
    DEFAULT_POSTGRES_DB_NAME: str = 'postgres'
    POSTGRES_DATABASE_URL = (
        f'{POSTGRES_DIALECT_DRIVER}://{POSTGRES_DB_USERNAME}:'
        f'{POSTGRES_DB_PASSWORD}@{POSTGRES_DB_HOST}:'
        f'{POSTGRES_DB_PORT}/{POSTGRES_DB_NAME}'
    )
    DEFAULT_POSTGRES_DATABASE_URL = (
        f'{POSTGRES_DIALECT_DRIVER}://{POSTGRES_DB_USERNAME}:'
        f'{POSTGRES_DB_PASSWORD}@{POSTGRES_DB_HOST}:'
        f'{POSTGRES_DB_PORT}/{DEFAULT_POSTGRES_DB_NAME}'
    )

    # JWT settings.
    authjwt_secret_key: str = os.getenv('authjwt_secret_key')
    authjwt_token_location: set = {os.getenv('authjwt_token_location')}
    authjwt_cookie_csrf_protect: bool = (os.getenv('authjwt_cookie_csrf_protect', 'False') == 'True')


CONFIGS = {
    ApiConstants.DEVELOPMENT_CONFIG.value: DevelopmentConfig,
    ApiConstants.TESTING_CONFIG.value: TestingConfig,
}


def get_app_config(config_name: str) -> BaseModel:
    """Get pydantic BaseModel class with application settings.

    Args:
        config_name: string with config name.

    Returns:
    App config from config mapping.
    """
    return CONFIGS[config_name]


class CeleryDevelopmentConfig:
    """Celery development environment variables."""

    CELERY_APP_NAME = os.getenv('CELERY_APP_NAME')
    C_FORCE_ROOT = os.getenv('C_FORCE_ROOT')
    accept_content = [os.getenv('CELERY_ACCEPT_CONTENT')]
    result_accept_content = [os.getenv('CELERY_RESULT_ACCEPT_CONTENT')]
    task_serializer = os.getenv('CELERY_TASK_SERIALIZER')
    result_serializer = os.getenv('CELERY_RESULT_SERIALIZER')
    backend = os.getenv('RESULT_BACKEND')
    broker = os.getenv('BROKER_URL')

    # AWS settings.
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
    AWS_S3_BUCKET_REGION = os.getenv('AWS_S3_BUCKET_REGION')

    # API settings.
    API_SQLALCHEMY_ECHO: bool = (os.getenv('API_SQLALCHEMY_ECHO', 'False') == 'True')
    API_SQLALCHEMY_FUTURE: bool = (os.getenv('API_SQLALCHEMY_FUTURE', 'False') == 'True')

    # Postgres settings.
    POSTGRES_DIALECT_DRIVER: str = os.getenv('POSTGRES_DIALECT_DRIVER')
    POSTGRES_DB_USERNAME: str = os.getenv('POSTGRES_DB_USERNAME')
    POSTGRES_DB_PASSWORD: str = os.getenv('POSTGRES_DB_PASSWORD')
    POSTGRES_DB_HOST: str = os.getenv('POSTGRES_DB_HOST')
    POSTGRES_DB_PORT: str = os.getenv('POSTGRES_DB_PORT')
    POSTGRES_DB_NAME: str = os.getenv('POSTGRES_DB_NAME')
    POSTGRES_DATABASE_URL = (
        f'{POSTGRES_DIALECT_DRIVER}://{POSTGRES_DB_USERNAME}:'
        f'{POSTGRES_DB_PASSWORD}@{POSTGRES_DB_HOST}:'
        f'{POSTGRES_DB_PORT}/{POSTGRES_DB_NAME}'
    )


class CeleryTestingConfig:
    """Celery testing environment variables."""

    CELERY_APP_NAME = os.getenv('CELERY_APP_NAME')
    C_FORCE_ROOT = os.getenv('C_FORCE_ROOT')
    accept_content = [os.getenv('CELERY_ACCEPT_CONTENT')]
    result_accept_content = [os.getenv('CELERY_RESULT_ACCEPT_CONTENT')]
    task_serializer = os.getenv('CELERY_TASK_SERIALIZER')
    result_serializer = os.getenv('CELERY_RESULT_SERIALIZER')
    backend = os.getenv('RESULT_BACKEND')
    broker = os.getenv('BROKER_URL')

    # AWS settings.
    AWS_ACCESS_KEY_ID = f'test_{os.getenv("AWS_ACCESS_KEY_ID")}'
    AWS_SECRET_ACCESS_KEY = f'test_{os.getenv("AWS_SECRET_ACCESS_KEY")}'
    AWS_S3_BUCKET_NAME = f'test_{os.getenv("AWS_S3_BUCKET_NAME")}'
    AWS_S3_BUCKET_REGION = os.getenv('AWS_S3_BUCKET_REGION')

    # API settings.
    API_SQLALCHEMY_ECHO: bool = (os.getenv('API_SQLALCHEMY_ECHO', 'False') == 'True')
    API_SQLALCHEMY_FUTURE: bool = (os.getenv('API_SQLALCHEMY_FUTURE', 'False') == 'True')

    # Postgres settings.
    POSTGRES_DIALECT_DRIVER: str = os.getenv('POSTGRES_DIALECT_DRIVER')
    POSTGRES_DB_USERNAME: str = os.getenv('POSTGRES_DB_USERNAME')
    POSTGRES_DB_PASSWORD: str = os.getenv('POSTGRES_DB_PASSWORD')
    POSTGRES_DB_HOST: str = os.getenv('POSTGRES_DB_HOST')
    POSTGRES_DB_PORT: str = os.getenv('POSTGRES_DB_PORT')
    POSTGRES_DB_NAME: str = 'test_postgres'
    POSTGRES_DATABASE_URL = (
        f'{POSTGRES_DIALECT_DRIVER}://{POSTGRES_DB_USERNAME}:'
        f'{POSTGRES_DB_PASSWORD}@{POSTGRES_DB_HOST}:'
        f'{POSTGRES_DB_PORT}/{POSTGRES_DB_NAME}'
    )


CELERY_CONFIGS = {
    CeleryConstants.DEVELOPMENT_CONFIG.value: CeleryDevelopmentConfig,
    CeleryConstants.TESTING_CONFIG.value: CeleryTestingConfig,
}


def get_celery_config(config_name: str) -> object:
    """Get object with celery application settings.

    Args:
        config_name: string with config name.

    Returns:
    object from celery config mapping.
    """
    return CELERY_CONFIGS[config_name]
