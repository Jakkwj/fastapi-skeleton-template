from datetime import (
    UTC,
    datetime,
    timedelta,
)
from traceback import format_exc

from authlib.jose import (
    JoseError,
    JWTClaims,
    jwt,
)

from app.exceptions.exception import AuthenticationError, AuthorizationError
from config.config import get_settings

settings = get_settings()


def create_token_from_user(user_id: int, expiration: int = 7200):
    """根据 user_id 生成 jwt token.

    默认 token 过期时间 7200s, 2h.
    设置过期时间是把 exp 放在 payload 中进行设置, 一起 encode
    'exp' 这个 key 不能修改
    然后 decode 后再 validate

    token_valid_key 的目的可以做到提前销毁 token, 但是这样需要每次都查询数据库
    先不用这个功能了 (2024.09.03)
    """
    header = {"alg": "HS256"}  # 签名算法
    key = settings.SECRET_KEY  # 用于签名的密钥
    expires_delta = timedelta(seconds=expiration)
    expires = datetime.now(tz=UTC) + expires_delta  # 设置过期时间
    payload = {  # 待签名的 payload
        "id": user_id,
        "exp": expires,  # 'exp' 不能修改
    }
    return jwt.encode(header=header, payload=payload, key=key).decode("utf-8")


async def decode_token(
    token: str,
) -> JWTClaims:
    """验证 token 是否有效.

    成功返回 payload JWTClaims 字典
    失败:
        expire: raise 403
        其它异常 raise 401
    """
    payload = None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        payload.validate()
    except JoseError as error:
        if "expired" in f"{error.error}":  # token 过期错误
            raise AuthorizationError(f"{error.error}")  # 403
        raise AuthenticationError(f"{error.error}")  # 401
    except Exception:  # 其它异常
        raise AuthenticationError(format_exc())  # 401

    return payload


async def decode_refresh_token(
    token: str,
) -> JWTClaims:
    """验证 token 是否有效.

    成功返回 payload JWTClaims 字典
    失败 raise 401
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        payload.validate()
    except Exception:
        raise AuthenticationError(format_exc())  # 401

    return payload
