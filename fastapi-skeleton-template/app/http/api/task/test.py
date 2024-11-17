from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.http.deps import (
    get_db_session,
    get_payload_from_token,
)
from app.services.task import publish_task
from app.tasks.task_test import task_test
from config.config import get_settings

settings = get_settings()
router = APIRouter(
    prefix="/task",
    dependencies=[Depends(get_payload_from_token)],  # 表示需要登录且激活, 即 login_required
)


@router.get("/test", response_class=ORJSONResponse)
async def token(
    request: Request,
    current_user: dict = Depends(get_payload_from_token),
    db: AsyncSession = Depends(get_db_session),
):
    """
    用户名 + 密码登录, 即实际上的 sign in.
    前端登录, 输入账号密码, 成功后前端获取 access_token 和 refresh_Token 2个 token
    sign out 直接在前端删除 token 即可
    """
    await publish_task(
        task_name="task_test",
        publisher=task_test,
        request=request,
    )
    return {"message": "task_test ok"}
