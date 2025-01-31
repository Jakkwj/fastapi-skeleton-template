from datetime import datetime
from traceback import format_exc

from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.http.deps import get_db_session
from app.models import User
from app.schemas.users import UserSignUp
from app.services.crypto import decrypt_data, verifier_sign
from config.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/user/sign")


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    UserSignUp: UserSignUp,
    db: AsyncSession = Depends(get_db_session),
):
    """Create a new user."""
    name = decrypt_data(UserSignUp.username)

    if verifier_sign(name, UserSignUp.sign):  # 验证签名通过, 说明是正确的前端发起的请求
        name = name.lower()  # 强制小写
        email = decrypt_data(UserSignUp.email).lower()  # 强制小写

        async with db as session:
            result = (
                await session.execute(select(User.id).where(User.name == name).limit(1))
            ).first()
            if result:
                return ORJSONResponse(
                    {"message": "User Name Already Exists. Please Enter a Different User Name."},
                    status_code=status.HTTP_226_IM_USED,
                )

            result = (
                await session.execute(select(User.id).where(User.email == email).limit(1))
            ).first()
            if result:
                return ORJSONResponse(
                    {"message": "Email Already Exists. Please Enter a Different Email."},
                    status_code=status.HTTP_226_IM_USED,
                )

        try:
            async with db as session:
                session.add(
                    User(
                        name=name,
                        email=email,
                        password=decrypt_data(UserSignUp.password),
                        created_timestamp=datetime.now(),
                    )
                )
                await session.commit()

            return ORJSONResponse(
                {
                    "message": "Sign Up Success! Please Check Your Email to Confirm your Account. If You don't Get the Email, Just Sign In and Get a New One."
                },
                status_code=status.HTTP_201_CREATED,
            )

        except Exception:
            logger.error(format_exc())
            return ORJSONResponse(
                {"message": "This User Name is being registered. Please Wait and Try Again."},
                status_code=status.HTTP_226_IM_USED,
            )

    else:
        return ORJSONResponse({"message": "Forbidden!"}, status_code=status.HTTP_403_FORBIDDEN)
