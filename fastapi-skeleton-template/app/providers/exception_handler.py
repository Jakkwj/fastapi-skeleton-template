from fastapi import (
    FastAPI,
    Request,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions.exception import (
    AuthenticationError,
    AuthorizationError,
)
from config.config import DevelopmentSettings, ProductionSettings


def register(
    app: FastAPI, settings: DevelopmentSettings | ProductionSettings
):  # settings: placeholder
    @app.exception_handler(AuthenticationError)
    async def authentication_exception_handler(request: Request, error: AuthenticationError):
        """
        认证异常处理
        """
        return ORJSONResponse(status_code=error.status_code, content={"message": error.message})

    @app.exception_handler(AuthorizationError)
    async def authorization_exception_handler(request: Request, error: AuthorizationError):
        """
        权限异常处理
        """
        return ORJSONResponse(status_code=error.status_code, content={"message": error.message})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        参数验证异常
        """
        logger.error({"message": exc.errors()[0]["msg"], "body": exc.body})
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"message": exc.errors()[0]["msg"], "body": exc.body}),
        )

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request: Request, exc):
        return ORJSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder({"message": str(exc.detail)}),
        )
