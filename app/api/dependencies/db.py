import sys
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import config
from app.db.configs.connection import AsyncDatabaseManager, db


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Returns a new session to the database
    """

    if "pytest" in sys.modules:
        test_db = AsyncDatabaseManager(config.TEST_DB_URL)
        test_db.connect()
        await test_db.create_tables()
        async with test_db as session:

            yield session

        await test_db.drop_tables()
        await session.close()

    async with db as session:
        yield session
