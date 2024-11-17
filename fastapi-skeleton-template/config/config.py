from functools import cache
from multiprocessing import cpu_count
from os import (
    environ,
    path,
)

from .settings.dir import get_work_dir
from .settings.email import Settings as EmailSettings
from .settings.logging import Settings as LoggingSettings
from .settings.redis import Settings as RedisSettings

_WORK_DIR = get_work_dir()


class Settings(EmailSettings, LoggingSettings, RedisSettings):
    NAME: str  # 通过 .env 自动获取
    ENV: str  # 通过 .env 自动获取

    SECRET_KEY: str  # 通过 .env 自动获取
    PUBLIC_KEY_CLIENT: str  # 通过 .env 自动获取
    PRIVATE_KEY_SERVER: str  # 通过 .env 自动获取

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    WORKERS: int = cpu_count()

    URL: str = "http://localhost"
    TIME_ZONE: str = "RPC"

    WORK_DIR: str = _WORK_DIR

    class Config:  # type: ignore
        env_file = f"{_WORK_DIR}.env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # 'forbid'


class DevelopmentSettings(Settings):
    FRONTEND_URL: str  # 通过 .env 自动获取
    DATABASE_URL: str  # 通过 .env 自动获取
    DATABASE_URL_SYNC: str  # 通过 .env 自动获取

    DEBUG: bool = True

    # token
    CONFIRM_TOKEN_EXPIRE: int = 300  # 注册确认邮箱 token 过期时间, 30s
    ACCESS_TOKEN_EXPIRE: int = 60  # access_token 过期时间, 1min
    REFRESH_TOKEN_EXPIRE: int = 1200  # refresh_Token 过期时间, 1h
    CALCULATION_TOKEN_EXPIRE: int = 3600  # refresh_Token 过期时间, 1h

    class Config:  # type: ignore
        env_file = f"{_WORK_DIR}.env", f"{_WORK_DIR}.env.development"
        env_file_encoding = "utf-8"
        extra = "ignore"  # 'forbid'


class ProductionSettings(Settings):
    FRONTEND_URL: str  # 通过 .env 自动获取
    DATABASE_URL: str  # 通过 .env 自动获取
    DATABASE_URL_SYNC: str  # 通过 .env 自动获取

    DEBUG: bool = False

    # token
    CONFIRM_TOKEN_EXPIRE: int = 3600  # 注册确认邮箱 token 过期时间, 1h
    ACCESS_TOKEN_EXPIRE: int = 7200  # access_token 过期时间, 2h
    REFRESH_TOKEN_EXPIRE: int = 604800  # refresh_Token 过期时间, 7d
    CALCULATION_TOKEN_EXPIRE: int = 60  # calculation_token 过期时间, 60s

    SSL_DISABLED: bool = False

    class Config:  # type: ignore
        env_file = f"{_WORK_DIR}.env", f"{_WORK_DIR}.env.production"
        env_file_encoding = "utf-8"
        extra = "ignore"  # 'forbid'


settings_dict = {
    "development": DevelopmentSettings,
    "production": ProductionSettings,
}


@cache
def get_settings() -> DevelopmentSettings | ProductionSettings:
    """lru_cache 保证了只有在第一次调用它时才会创建 Settings 对象一次
        https://fastapi.tiangolo.com/zh/advanced/settings/#__tabbed_4_1

        .env 中 ENV 决定了开发环境

    Returns:
        _type_: _description_
    """
    from dotenv import load_dotenv

    dotenv_path = path.join(_WORK_DIR, ".env")

    if path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        if env := environ.get("ENV"):
            return settings_dict[env]()
        else:
            return settings_dict["development"]()
    else:
        return settings_dict["development"]()
