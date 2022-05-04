from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def create_engine(database_url: str, echo: bool, future: bool) -> AsyncEngine:
    """Create sqlalchemy async engine.

    Args:
        database_url: postgres database url.
        echo: sqlalchemy echo logs.
        future: sqlalchemy future bool.

    Returns:
    newly created AsyncEngine instance.
    """
    return create_async_engine(database_url, echo=echo, future=future)


async def get_session(request: Request) -> AsyncSession:
    """Creates sqlalchemy async session based on config from request app.

    Args:
        request: fastapi Request object.

    Returns:
    newly created AsyncSession instance.
    """
    engine = create_engine(
        database_url=request.app.app_config.POSTGRES_DATABASE_URL,
        echo=request.app.app_config.API_SQLALCHEMY_ECHO,
        future=request.app.app_config.API_SQLALCHEMY_FUTURE,
    )
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
        await session.close()
        await engine.dispose()
