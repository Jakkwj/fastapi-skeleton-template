from fastapi import APIRouter

from app.http.api.task import test
from app.http.api.users import (
    auth,
    sign,
)

api_router = APIRouter()
api_router.include_router(auth.router, tags=["user"])
api_router.include_router(sign.router, tags=["user"])
api_router.include_router(test.router, tags=["task"])
