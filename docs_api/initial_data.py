import asyncio
import logging

from docs_app.core.security import get_password_hash
from docs_app.db.async_session import async_session, engine
from docs_app.db.models.base import Base
from docs_app.db.models.db_models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    async with engine.begin() as db_conn:
        await db_conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        session.add(
            User(
                username="super",
                full_name="super",
                hashed_password=get_password_hash("super"),
            )
        )
        await session.commit()


async def async_main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(async_main())
