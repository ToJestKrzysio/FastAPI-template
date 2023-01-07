import asyncio
from asyncio import current_task

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_scoped_session
from sqlalchemy.orm import sessionmaker

from db import orm


@pytest.fixture(scope="session", autouse=True)
def engine() -> AsyncEngine:
    yield create_async_engine(
        'sqlite+aiosqlite://', future=True, echo=False, connect_args={"check_same_thread": False}
    )


@pytest.fixture(scope="session", autouse=True)
def async_session_maker(engine):
    yield async_scoped_session(
        sessionmaker(engine, expire_on_commit=False, class_=AsyncSession), scopefunc=current_task
    )


@pytest.fixture(scope="function")
def migrated_db(engine):
    async def create_all():
        async with engine.begin() as conn:
            await conn.run_sync(orm.Base.metadata.drop_all)
            await conn.run_sync(orm.Base.metadata.create_all)

    async def drop_all():
        async with engine.begin() as conn:
            await conn.run_sync(orm.Base.metadata.drop_all)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_all())
    del loop

    yield

    loop = asyncio.get_event_loop()
    loop.run_until_complete(drop_all())
    del loop
