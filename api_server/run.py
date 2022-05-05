import uvicorn
from app import create_app
from app.config import Settings

app = create_app()
app_settings = Settings()


if __name__ == "__main__":
    file_name = __file__.split('/')[-1].replace('.py', '')
    uvicorn.run(
        f"{file_name}:app",
        host=app_settings.API_SERVER_HOST,
        port=app_settings.API_SERVER_PORT,
        log_level=app_settings.API_SERVER_LOG_LEVEL,
        reload=app_settings.API_SERVER_RELOAD,
    )
