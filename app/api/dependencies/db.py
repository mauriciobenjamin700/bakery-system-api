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

        test_db = AsyncDatabaseManager(config.DB_URL_TEST)

        test_db.connect()

        await test_db.create_tables()

        session = await test_db.get_session()
    else:
        async with db as session:
            session = await db.get_session()
            yield session
