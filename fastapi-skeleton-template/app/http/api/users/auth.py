from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import AuthenticationError
from app.http.deps import (
    get_current_user,
    get_db_session,
    get_payload_from_token,
    oauth2_scheme,
)
from app.schemas.users import SignToken, Token
from app.services.auth.grant import password_grant
from app.services.auth.jwt_helper import create_token_from_user, decode_refresh_token
from app.services.crypto import encrypt_data, sign_data, verifier_sign
from config.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/user/auth")


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def token(
    request_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session),
) -> Token:
    """
    用户名 + 密码登录, 即实际上的 sign in.
    前端登录, 输入账号密码, 成功后前端获取 access_token 和 refresh_Token 2个 token
    sign out 直接在前端删除 token 即可
    """
    token = await password_grant(request_data, db)
    return Token(**token)


@router.post("/refresh_token", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh_token(
    SignToken: SignToken,
    token: str = Depends(oauth2_scheme),
) -> Token | None:
    """如果 accessToken 过期, 用 refreshToken 再次生成新的 accessToken 和 refreshToken.

    403 是 accessToken 过期, 进入本路由:
        成功, 200, 返回新的 accessToken 和 refreshToken
        失败, 401, refreshToken 过期/验证签名失败
    """
    if verifier_sign(token, SignToken.sign):  # 验证签名通过, 说明是正确的前端发起的请求
        payload = await decode_refresh_token(token)  # 成功返回 payload, 失败 401 返回给前端
        user_id: int = payload.get("id")  # type: ignore
        access_token = create_token_from_user(user_id, settings.ACCESS_TOKEN_EXPIRE)
        refresh_Token = create_token_from_user(user_id, settings.REFRESH_TOKEN_EXPIRE)

        return Token(
            **{
                "token_type": "bearer",
                "access_token": encrypt_data(access_token),
                "refresh_token": encrypt_data(refresh_Token),
                "sign": sign_data(access_token),
            }
        )

    else:
        raise AuthenticationError("Signature does not mismatch!")  # 401


@router.get("/current_user", response_class=ORJSONResponse)
async def current_user(
    current_user: dict = Depends(get_payload_from_token),
    db: AsyncSession = Depends(get_db_session),
):
    """
    测试: 获取当前用户信息
    """
    return {"current_user": current_user}
