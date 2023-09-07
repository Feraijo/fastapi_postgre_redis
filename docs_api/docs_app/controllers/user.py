from typing import Optional

from docs_app.core.security import get_password_hash, verify_password
from docs_app.db.models.db_models import User
from docs_app.schemas.user import UserCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserController:
    async def get(self, db: AsyncSession, id: int) -> Optional[User]:
        result = await db.scalars(select(User).filter(User.id == id))
        return result.first()

    async def get_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        user = await db.scalars(select(User).where(User.username == username))
        return user.first()

    async def create(self, db: AsyncSession, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
        )
        db.add(db_obj)
        await db.commit()
        db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: AsyncSession, username: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user_controller = UserController()
