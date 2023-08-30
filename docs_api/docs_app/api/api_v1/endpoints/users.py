from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import Result, select
#from docs_app.crud import user
from docs_app import crud
from docs_app.schemas import UserSchema, UserCreate, UserUpdate
from docs_app.db.models.base import Base
from docs_app.core import security
from docs_app.db.models.db_models import User
from docs_app.api import deps
from docs_app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated

router = APIRouter()


@router.post("/register", response_model=UserSchema)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_username(db, user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await crud.user.create(db, obj_in=user_in)
    return user
