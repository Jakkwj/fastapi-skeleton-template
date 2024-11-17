from uvicorn import run

from bootstrap.application import create_app
from config.config import get_settings

settings = get_settings()
app = create_app()


if __name__ == "__main__":
    """
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple uv
    uv pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastapi numpy pandas icecream pyyaml matplotlib seaborn "uvicorn[standard]" python-dotenv pydantic_settings pyjwt "passlib[bcrypt]"
    启动服务器
        - python -m uvicorn main:app --reload
        - python main.py
        - fastapi dev
        - fastapi run  # 不会 reload

    main:app  文件名: FastAPI() 实例
    """
    run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
    )
