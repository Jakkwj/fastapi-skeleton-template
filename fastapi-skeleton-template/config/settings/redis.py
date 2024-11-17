from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0  # 0-15
    REDIS_EXPIRE: int = 60  # 过期时间, 60s
