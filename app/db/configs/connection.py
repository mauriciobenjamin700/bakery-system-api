from typing import Optional

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from app.core.settings import config
from app.db.configs.base import Base
from app.db.models import *


class AsyncDatabaseManager:
    """
    A class to manage the connection to the database.
    It handles the creation and disposal of the database engine and sessions.
    It also provides methods to create and drop tables in the database.
    Attributes:
        db_url (str): The database URL.
        _engine (AsyncEngine): The SQLAlchemy async engine.
        _session_maker (async_sessionmaker): The SQLAlchemy async session maker.
        _active_session (AsyncSession): The active database session.
    Methods:
        connect(): Connect to the database.
        disconnect(): Disconnect from the database.
        get_session(): Get or reuse an active database session.
        create_tables(): Create all tables in the database.
        drop_tables(): Drop all tables in the database.
    """

    def __init__(self, db_url: str = config.DB_URL) -> None:
        self.db_url = db_url
        self._engine: Optional[AsyncEngine] = None
        self._session_maker: Optional[async_sessionmaker] = None
        self._active_session: Optional[AsyncSession] = None  # Sessão ativa

    async def connect(self) -> None:
        """Connect to the database."""
        if self._engine is None:
            if "sqlite" in self.db_url:
                self._engine = create_async_engine(
                    self.db_url,
                    echo=False,
                    connect_args={"check_same_thread": False},
                )
            else:
                self._engine = create_async_engine(
                    self.db_url, echo=False, pool_size=10, max_overflow=5
                )

            self._session_maker = async_sessionmaker(
                self._engine, expire_on_commit=False, class_=AsyncSession
            )

    async def disconnect(self) -> None:
        """Disconnect from the database."""
        if self._active_session is not None:
            await self._active_session.close()
            self._active_session = None

        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._session_maker = None

    async def get_session(self) -> AsyncSession:
        """Get or reuse an active database session."""
        if self._active_session is None:
            if self._session_maker is None:
                await self.connect()
            self._active_session = self._session_maker()

        return self._active_session

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


# Initialize the database manager
db = AsyncDatabaseManager(config.DB_URL)
