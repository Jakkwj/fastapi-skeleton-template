from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import AuthenticationError
from app.models import User
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
    async with db as session:
        result = await session.execute(
            select(User).where(User.name == decrypt_data(request_data.username))
        )
        user = result.scalars().first()  # 第一条数据

        if not user:  # 用户名校验
            raise AuthenticationError(
                message="Invalid username, please try again.",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )  # 406
        if not (user.verify_password(decrypt_data(request_data.password))):  # 用户密码校验
            raise AuthenticationError(
                message="Wrong password, please try again.",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )  # 406

        access_token = user.create_token(settings.ACCESS_TOKEN_EXPIRE)  # type: ignore
        refresh_Token = user.create_token(settings.REFRESH_TOKEN_EXPIRE)  # type: ignore
        await session.commit()

    return {
        "token_type": "bearer",
        "access_token": encrypt_data(access_token),
        "refresh_token": encrypt_data(refresh_Token),
        "sign": sign_data(access_token),
    }
