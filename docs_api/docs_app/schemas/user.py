from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserSchema(UserBase):
    pass
