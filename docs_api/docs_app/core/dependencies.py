from typing import Generator
import aioredis
from fastapi import Depends, HTTPException, status, Request
#from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from docs_app.controllers.user import user_controller
from docs_app.schemas import TokenPayload
from docs_app.db.models.db_models import User
from docs_app.core.config import settings
from docs_app.db.async_session import async_session
from docs_app.redis.redis_session_storage import SessionStorage
from uuid import uuid4
import json

#reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")

def genSessionId() -> str:
    return uuid4().hex


async def get_db() -> Generator[AsyncSession, None, None]:
    async with async_session() as session:
        yield session


async def get_redis():
    redis = SessionStorage()
    return redis

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    redis = Depends(get_redis),
    #token: str = Depends(reusable_oauth2)
) -> User:
    try:
        sessionId = request.cookies.get(settings.SSID, "")
        token = await redis.read_session(sessionId)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorised, use /login/access-token",
        )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await user_controller.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

