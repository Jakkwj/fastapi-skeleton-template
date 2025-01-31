from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import (
    check_password_hash,
)

from app.exceptions.exception import AuthenticationError
from app.models import User
from app.services.auth.jwt_helper import create_token_from_user
from app.services.crypto import decrypt_data, encrypt_data, sign_data
from config.config import get_settings

settings = get_settings()


async def password_grant(
    request_data: OAuth2PasswordRequestForm, db: AsyncSession
) -> dict[str, str]:
    """用户密码授权, 生成 token.

    验收通过后, 生成 access_token 和 refresh_token.

    Args:
        request_data (OAuth2PasswordRequestForm): _description_
        db (AsyncSession): _description_

    Raises:
        AuthenticationError: _description_
        AuthenticationError: _description_

    Returns:
        dict[str, str]: _description_
    """

    user_name = decrypt_data(request_data.username)

    async with db as session:
        result = (
            await session.execute(
                select(User.id, User.email, User.password_hash)  # type: ignore
                .where(User.name == user_name)
                .limit(1)
            )
        ).first()

        if result:
            user_id, user_email, user_password_hash = result
        else:  # 如果没有找到 用户名 则尝试用 email 登录
            result = (
                await session.execute(
                    select(User.id, User.email, User.password_hash)  # type: ignore
                    .where(User.email == user_name)
                    .limit(1)
                )
            ).first()

        if result:
            user_id, user_email, user_password_hash = result

        else:  # 用户名校验
            raise AuthenticationError(
                message="Invalid username, please try again.",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )
        if not (
            check_password_hash(user_password_hash, decrypt_data(request_data.password))
        ):  # 用户密码校验
            raise AuthenticationError(
                message="Wrong password, please try again.",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )

        access_token: str = create_token_from_user(user_id, expiration=settings.ACCESS_TOKEN_EXPIRE)
        refresh_Token: str = create_token_from_user(
            user_id, expiration=settings.REFRESH_TOKEN_EXPIRE
        )
        await session.commit()

    return {
        "token_type": "bearer",
        "access_token": encrypt_data(access_token),
        "refresh_token": encrypt_data(refresh_Token),
        "sign": sign_data(access_token),
    }
