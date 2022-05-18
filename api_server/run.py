import uvicorn
from app import create_app
from common.constants.api import ApiConstants

app = create_app(config_name=ApiConstants.DEVELOPMENT_CONFIG.value)


if __name__ == "__main__":
    file_name = __file__.split('/')[-1].replace('.py', '')
    uvicorn.run(
        f"{file_name}:app",
        host=app.app_config.API_SERVER_HOST,
        port=app.app_config.API_SERVER_PORT,
        log_level=app.app_config.API_SERVER_LOG_LEVEL,
        reload=app.app_config.API_SERVER_RELOAD,
    )
