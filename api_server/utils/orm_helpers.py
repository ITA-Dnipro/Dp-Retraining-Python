from contextlib import asynccontextmanager
from typing import AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


@asynccontextmanager
async def create_db_session(engine: AsyncEngine) -> AsyncContextManager:
    """Creates sqlalchemy AsyncSession instance within async context manager.

    Args:
        engine: instance of sqlalchemy AsyncEngine.

    Returns:
    An AsyncSession object within async context manager.
    """
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False,
    )
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            await engine.dispose()
