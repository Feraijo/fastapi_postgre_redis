from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from docs_app.core.config import settings

engine = create_async_engine(settings.CONN_STRING, echo=True)

async_session: Callable[[], AsyncSession] = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
