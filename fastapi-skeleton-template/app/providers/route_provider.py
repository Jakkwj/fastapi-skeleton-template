from fastapi import FastAPI
from loguru import logger

from routes.api import api_router


def boot(app: FastAPI):
    # 注册api路由[routes/api.py]
    app.include_router(api_router, prefix="/api/v1")

    if app.debug:
        for route in app.routes:
            logger.info(route)
