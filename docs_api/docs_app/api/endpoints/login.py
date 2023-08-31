from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from docs_app.schemas import TokenSchema
from docs_app.controllers.user import user_controller
from docs_app.core.dependencies import get_db, get_redis
from docs_app.core import security
from docs_app.core.config import settings


router = APIRouter()


@router.post("/login/access-token", response_model=TokenSchema)
async def login_access_token(
    response: Response,
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    redis = Depends(get_redis),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_controller.get_by_username(db, form_data.username)
    user = await user_controller.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
    sessionId = await redis.write_session(token)
    response.set_cookie(settings.SSID, sessionId, httponly=True)
    return token
