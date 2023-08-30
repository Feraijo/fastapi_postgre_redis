from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy import Result, select

from docs_app.core.security import get_password_hash, verify_password
from docs_app.crud.base import CRUDBase
#from docs_app.models.user import User
from docs_app.db.models.db_models import User
from docs_app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_username(self, db: Session, username: str) -> Optional[User]:
        user = await db.scalars(select(User).where(User.username == username))
        return user.first()

    async def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
        )
        db.add(db_obj)
        await db.commit()
        db.refresh(db_obj)
        return db_obj

    async def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        user = await self.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

user = CRUDUser(User)
