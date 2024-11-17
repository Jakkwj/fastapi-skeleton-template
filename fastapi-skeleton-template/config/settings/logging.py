from pydantic_settings import BaseSettings

from .dir import get_work_dir

_WORK_DIR = get_work_dir()


class Settings(BaseSettings):
    """
    配置参考loguru
    """

    LOG_LEVEL: str = "DEBUG"
    LOG_ROTATION: str = "00:00"
    LOG_RETENTION: str = "14 days"

    LOG_PATH: str = f"{_WORK_DIR}storage/logs/fastapi-{{time:YYYY-MM-DD}}.log"

    LOG_LEVEL_ERROR: str = "ERROR"  # 只看 ERROR
    LOG_PATH_ERROR: str = f"{_WORK_DIR}storage/logs/error/fastapi-{{time:YYYY-MM-DD}}.log"

    class Config:
        env_file = f"{_WORK_DIR}.env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # 'forbid'
