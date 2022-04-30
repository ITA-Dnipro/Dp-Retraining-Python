import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    """Stores all project settings."""

    # App settings.
    API_SERVER_HOST: str = os.getenv('API_SERVER_HOST')
    API_SERVER_PORT: int = int(os.getenv('API_SERVER_PORT'))
    API_SERVER_LOG_LEVEL: str = os.getenv('API_SERVER_LOG_LEVEL')
    API_SERVER_RELOAD: bool = (os.getenv('API_SERVER_RELOAD', 'False') == 'True')

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
