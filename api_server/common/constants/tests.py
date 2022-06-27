import enum


class GenericTestConstants(enum.Enum):
    """Generic tests constants."""
    # SQL Queries.
    SELECT_DATABASE_QUERY = "select * from pg_database where datname='{db_name}';"
    DELETE_DATABASE_QUERY = 'drop database {db_name};'
    CREATE_DATABASE_QUERY = 'create database {db_name};'
    # Alembic variables.
    ALEMBIC_MIGRATIONS_FOLDER = '/migrations'
    ALEMBIC_INI_FILENAME = 'alembic.ini'
    ROOT_FILEPATH = '/'
    SQLALCHEMY_URL_OPTION = 'sqlalchemy.url'
    SCRIPT_LOCATION_OPTION = 'script_location'
    ALEMBIC_HEAD = 'head'
    # AsyncClient stuff.
    BASE_URL_TEMPLATE = 'http://{api_host}:{api_port}'
    TEST_CLIENT_HEADERS = {'Content-Type': 'application/json'}


class HealthChecksConstants(enum.Enum):
    """Health checks constants."""

    ROOT_FILEPATH = '/'
    API_SERVER_STARTUP_FILENAME = 'api_server_startup.py'
    STDOUT_TIMEOUT_SEC = 10
