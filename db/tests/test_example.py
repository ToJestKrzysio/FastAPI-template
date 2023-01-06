from asyncio import current_task

import pytest
from sqlalchemy import Column, String, Integer, SmallInteger, select
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_scoped_session, \
    AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(SmallInteger)


@pytest.fixture(scope="module", autouse=True)
def engine() -> AsyncEngine:
    yield create_async_engine(
        'sqlite+aiosqlite://', future=True, echo=True, connect_args={"check_same_thread": False}
    )


@pytest.fixture(scope="module", autouse=True)
async def migrate_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="module", autouse=True)
async def async_session_maker(engine, migrate_db):
    await migrate_db.__anext__()
    yield async_scoped_session(
        sessionmaker(engine, expire_on_commit=False, class_=AsyncSession), scopefunc=current_task
    )


@pytest.mark.asyncio
async def test_get(async_session_maker):
    # await migrate_db.__anext__()  # Removing this line causes "sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: items"
    session_maker = await async_session_maker.__anext__()
    async with session_maker() as session:
        await session.execute(
            "INSERT INTO items (id, name, quantity) VALUES "
            '(0, "crowbar", 13),'
            '(1, "lamp", 94)'
        )
        stmt = select(Item).where(Item.id == 1)
        rows = await session.execute(stmt)
        result = rows.scalar_one()

        assert result.id == 1
        assert result.name == "lamp"
        assert result.quantity == 94
