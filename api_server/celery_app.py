from celery import Celery

from app.config import get_celery_config
from common.constants.celery import CeleryConstants


def create_celery_app(config_name=CeleryConstants.DEVELOPMENT_CONFIG.value):
    config = get_celery_config(config_name)

    app = Celery(
        main=config.CELERY_APP_NAME,
        backend=config.backend,
        broker=config.broker,
    )

    app.config_from_object(config)
    return app


app = create_celery_app()
