from contextlib import asynccontextmanager

from aioredis import from_url
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.models import Base  # 创建表的关键
from app.providers.database import engine
from config.config import DevelopmentSettings, ProductionSettings, get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """before yield 服务器开始之前, after yield 服务器结束后运行的命令

    Storing object instances in the app context: https://github.com/fastapi/fastapi/issues/81

    https://www.cnblogs.com/weiweivip666/p/18041474
    1.python3.11版本, aioredis 2.0.1版本, redis 7.x版本
    启动连接时会报一个TypeError: duplicate base class TimeoutError的错误
    问了Copilot, 说是兼容性问题, 在 Python3.11 中, asyncio.TimeoutError 被移动到了 asyncio.exceptions 模块中, 而 aioredis 库没有及时更新以适应这个变化。
    所以我们找到aioredis目录下的exceptions.py文件, 定位到14行代码
    class TimeoutError(asyncio.TimeoutError, builtins.TimeoutError, RedisError):
        pass

    所以我们修改为如下代码, 即可运行
    class TimeoutError(asyncio.exceptions.TimeoutError, RedisError):
        pass

    Args:
        app (FastAPI): _description_
    """
    logger.info("Application starting...")

    app.task_dict = {}  # type: ignore  注册全局变量获取异步任务实例

    app.redis = from_url(  # type: ignore
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
        encoding="utf-8",
        decode_responses=True,  # 默认返回的结果为 bytes, 设置 decode_responses 表示解码为字符串
    )  # 创建的是线程池对象

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )  # 检查数据库中是否存在相应的表, 如不存在则创建

    yield
    await engine.dispose()  # 关闭数据库连接
    app.redis.close()  # type: ignore 关闭 redis 连接

    logger.info("Application stopping...")


def add_global_middleware(app: FastAPI, settings):
    """
    注册全局中间件
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            settings.FRONTEND_URL,  # https://dash.simpowater.org, http://127.0.0.0:9000
        ],  # 允许的来源列表, 不要简单地使用 ["*"] 来允许所有来源, 可能带来安全风险
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register(app: FastAPI, settings: DevelopmentSettings | ProductionSettings):
    app.debug = settings.DEBUG
    app.title = settings.NAME

    add_global_middleware(app, settings)
