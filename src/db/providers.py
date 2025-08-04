from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.sql.expression import text

from helpers.logging import logger


class DataAsyncProvider:
    def __init__(self, db_url: str):
        self.url = db_url
        self.engine = create_async_engine(self.url, echo=False, future=True)
        self.async_session_factory = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_factory() as session:
            yield session

    @asynccontextmanager
    async def async_session_manager(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_factory() as session:
            yield session

    async def is_connected(self) -> bool:
        try:
            async with self.async_session_manager() as session:
                await session.execute(text("SELECT 1"))
            return True
        except Exception as ex:
            logger.exception(ex)
            return False
