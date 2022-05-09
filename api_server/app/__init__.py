from fastapi import FastAPI
from common.constants.api import ApiVersion
from hello_world import hello_world_router


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(hello_world_router, prefix=f'/api/v{ApiVersion.V1.value}')

    return app
