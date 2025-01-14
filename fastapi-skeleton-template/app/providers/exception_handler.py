from traceback import format_exception
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


def get_router_root(request_url) -> str:
    """获取请求的根 URL"""
    return f"{request_url.scheme}://{request_url.hostname}:{request_url.port}"


def register(
    app: FastAPI, settings: DevelopmentSettings | ProductionSettings
):  # settings: placeholder
    @app.exception_handler(AuthenticationError)
    async def authentication_exception_handler(
        request: Request, error: AuthenticationError
    ):
        """
        认证异常处理
        """
        return ORJSONResponse(
            status_code=error.status_code, content={"message": error.message}
        )

    @app.exception_handler(AuthorizationError)
    async def authorization_exception_handler(
        request: Request, error: AuthorizationError
    ):
        """
        权限异常处理
        """
        return ORJSONResponse(
            status_code=error.status_code, content={"message": error.message}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """
        参数验证异常
        """
        tb = "".join(
            format_exception(type(exc), exc, exc.__traceback__)
        )  # 获取完整的堆栈跟踪信息
        logger.error(f"Request to {request.url} caused an exception:\n{tb}")

        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {
                    "message": f"{exc.errors()[0]['msg']}. ({str(request.url).replace(get_router_root(request.url), '')})",
                    "body": exc.body,
                }
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request: Request, exc):
        tb = "".join(
            format_exception(type(exc), exc, exc.__traceback__)
        )  # 获取完整的堆栈跟踪信息
        logger.error(f"Request to {request.url} caused an exception:\n{tb}")

        return ORJSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(
                {
                    "message": f"{exc.detail}. ({str(request.url).replace(get_router_root(request.url), '')})",
                    "body": exc.body,
                }
            ),
        )
