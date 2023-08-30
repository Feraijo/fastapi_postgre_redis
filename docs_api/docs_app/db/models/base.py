from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any

from docs_app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncAttrs


@as_declarative()
class Base(AsyncAttrs):
    __abstract__ = True
    __table_args__ = {"schema": settings.DB_SCHEMA}