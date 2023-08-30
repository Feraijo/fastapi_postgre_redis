from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from docs_app.controllers.user import user_controller
from docs_app.schemas import UserSchema, UserCreate

from docs_app.core.dependencies import get_db

from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.post("/register", response_model=UserSchema)
async def register_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Зарегистрировать пользователя.
    """
    user = await user_controller.get_by_username(db, user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await user_controller.create(db, obj_in=user_in)
    return user
