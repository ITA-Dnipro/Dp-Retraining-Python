import os

from dotenv import load_dotenv

load_dotenv()

API_SERVER_URL = f'http://{os.getenv("API_SERVER_HOST")}:{os.getenv("API_SERVER_PORT")}'

VALID_UVICORN_STDOUT_MSG = f'INFO:     Uvicorn running on {API_SERVER_URL} (Press CTRL+C to quit)'
VALID_FASTAPI_STARTUP_STDOUT_MSG = 'INFO:     Application startup complete.'
