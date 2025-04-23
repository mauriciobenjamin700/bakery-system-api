from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.configs.connection import db


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Returns a new session to the database
    """
    async with db as session:
        yield session
