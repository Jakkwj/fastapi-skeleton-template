from pydantic_settings import BaseSettings

from .dir import get_work_dir

_WORK_DIR = get_work_dir()


class Settings(BaseSettings):
    SENDGRID_API_KEY: str
    SENDGRID_TEMPLATE_ID_CONFIRM: str
    SENDGRID_TEMPLATE_ID_FORGET_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file = f"{_WORK_DIR}.env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # 'forbid'
