from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from typing import Optional

from app.core.settings import config
from app.db.configs.base import Base
from app.db.models import *


class AsyncDatabaseManager:
    """
    A class to represent an async database manager. It is used to manage the database connection and session.

    - Args:
        - db_url: str = config.DB_URL
    - Attributes:
        - db_url: str
        - _engine: Optional[AsyncEngine]
        - _session_maker: Optional[async_sessionmaker]
        - _session: Optional[AsyncSession]
    - Methods:
        - connect: Connect to the database.
        - disconnect: Disconnect from the database.
        - create_tables: Create all tables in the database.
        - drop_tables: Drop all tables in the database.
        - __aenter__: Enter the async context manager.
        - __aexit__: Exit the async context manager.
    - Raises:
        - Exception: If the database connection fails.
    """
    def __init__(self, db_url: str = config.DB_URL) -> None:
        self.db_url = db_url
        self._engine: Optional[AsyncEngine] = None
        self._session_maker: Optional[async_sessionmaker] = None

    async def connect(self) -> None:
        """Connect to the database."""
        if self._engine is None:
            if "sqlite" in self.db_url:
                # SQLite specific configuration
                self._engine = create_async_engine(
                    self.db_url,
                    echo=False,
                    connect_args={"check_same_thread": False}
                )
            else:
                # Configuration for other databases
                self._engine = create_async_engine(
                    self.db_url,
                    echo=False,
                    pool_size=10,
                    max_overflow=5
                )

            self._session_maker = async_sessionmaker(
                self._engine,
                expire_on_commit=False,
                class_=AsyncSession
            )

    async def disconnect(self) -> None:
        """Disconnect from the database."""
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._session_maker = None


    async def create_tables(self) -> None:
        """Create all tables in the database."""
        if self._engine is None:
            await self.connect()

        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self) -> None:
        """Drop all tables in the database."""
        if self._engine is None:
            await self.connect()

        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def __aenter__(self) -> AsyncSession:
        """Enter the async context manager."""
        if self._session_maker is None:
            await self.connect()
        self._session = self._session_maker()
        return self._session

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """Exit the async context manager."""
        if hasattr(self, '_session'):
            await self._session.close()
        await self.disconnect()


# Initialize the database manager
db = AsyncDatabaseManager(config.DB_URL)
