from sqlalchemy.ext.asyncio import AsyncSession

from db import config


async def get_session() -> AsyncSession:
    async with config.async_session_maker() as session:
        yield session
