from datetime import datetime

from icecream import ic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import (
    User,
)
from config.config import get_settings

settings = get_settings()
ic.configureOutput(includeContext=True)  # print with line number


def _get_sync_session():
    engine = create_engine(settings.DATABASE_URL_SYNC)  # 同步引擎, 初始化数据库表时使用
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """使用同步引擎件导入进行初始化数据库. 在根目录的 main.py 运行."""

    SessionLocal = _get_sync_session()
    session = SessionLocal()

    user = User(
        name="test",
        email="test@test.com",
        password="test",  # type: ignore
        confirmed=True,
        created_timestamp=datetime.now(),  # type: ignore
    )
    session.add(user)
    session.commit()


if __name__ == "__main__":
    """
    # 使用命令alembic revision --autogenerate -m "备注", 生成当前的版本
    python -m alembic revision --autogenerate -m "init_db"

    # 使用命令alembic upgrade head将alembic的版本更新到最新版
    python -m alembic upgrade head
    """
    init_db()
