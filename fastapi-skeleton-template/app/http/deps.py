from collections.abc import AsyncGenerator

from authlib.jose import (
    JWTClaims,
)
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.providers.database import async_session
from app.services.auth.jwt_helper import decode_token
from app.services.auth.users import get_auth_user_from_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/user/auth/token"
)  # 自动提取 bearer 后的 token


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """获取异步 db session."""
    session = None
    try:
        async with async_session() as session:
            yield session
    finally:
        if session:
            await session.close()


async def get_payload_from_token(token: str = Depends(oauth2_scheme)) -> JWTClaims:
    """解码 token 后获取其中的信息, 可用于验证 token, 相当于 login_require.

    此时, payload.get('id') 即 user.id.
    这种方式并没有查询数据库, 只要 decode 成功就可获取 user.id
    如果仅仅需要 user.id 用这个方法更快, 因为没有查询数据库.
    如果需要 User, 则需要用 get_current_user.

    Args:
        token: 自动提取 bearer 后的 token.

    Raise:
        decode_token 失败会 401/403
    """
    return await decode_token(token)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db_session),
):
    """验证 token 后, 获取已经激活的授权用户.

    Args:
        token: 自动提取 bearer 后的 token.

    Raise:
        decode_token 失败会 401/403
        user 不存在会 401 AuthenticationError('User does not exist.')
    """
    return await get_auth_user_from_token(token, db)
