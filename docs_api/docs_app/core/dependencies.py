from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from docs_app.controllers.user import user_controller
from docs_app.schemas import TokenPayload
from docs_app.db.models.db_models import User
from docs_app.core.config import settings
from docs_app.db.async_session import async_session

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/access-token")

async def get_db() -> Generator[AsyncSession, None, None]:
    async with async_session() as session:
        yield session


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
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
