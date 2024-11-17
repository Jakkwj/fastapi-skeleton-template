from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.exceptions.exception import AuthenticationError
from app.models import User
from app.services.auth.jwt_helper import (
    decode_token,
)


async def get_auth_user_from_token(
    token: str,
    db: AsyncSession,
) -> User | None:
    """获取已经 confirmed 的用户.
    注意, 并没有比较 token_valid_key.
    """
    payload = await decode_token(token)  # 成功返回 payload, 失败 401/403 返回给前端
    async with db as session:
        result = await session.execute(select(User).where(User.id == payload.get("id")))  # type: ignore
        user = result.scalars().first()  # 第一条数据

        if not user:
            raise AuthenticationError("User does not exist.")  # 401
        if not user.confirmed:  # type: ignore
            raise AuthenticationError("User unconfirmed.", status.HTTP_423_LOCKED)

        return user
