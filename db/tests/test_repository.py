# from asyncio import current_task
#
# import pytest
# from sqlalchemy import event
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_scoped_session
# from sqlalchemy.orm import sessionmaker
#
# from db import orm, models
# from db.repository import ItemRepository
#
#
# @pytest.fixture(scope="session", autouse=True)
# def engine() -> AsyncEngine:
#     yield create_async_engine(
#         'sqlite+aiosqlite://', future=True, echo=True, connect_args={"check_same_thread": False}
#     )
#
#
# @pytest.fixture(scope="session", autouse=True)
# async def migrate_db(event_loop):
#     async with engine.begin() as conn:
#         await conn.run_sync(orm.Base.metadata.drop_all)
#         await conn.run_sync(orm.Base.metadata.create_all)
#
#
# @pytest.fixture(scope="session", autouse=True)
# def async_session_maker(engine):
#     yield async_scoped_session(
#         sessionmaker(engine, expire_on_commit=False, class_=AsyncSession), scopefunc=current_task
#     )
#
#
# @pytest.fixture(scope="function", autouse=True)
# async def async_session(async_session_maker, engine) -> AsyncSession:
#     connection = engine.connect()
#     trans = await connection.begin()
#     session = async_session_maker(bind=connection)
#     nested = connection.begin_nested()
#
#     @event.listens_for(session, "after_transaction_end")
#     def end_savepoint(_session, _transaction):
#         nonlocal nested
#         if not nested.is_active:
#             nested = connection.begin_nested()
#
#     async with async_session_maker() as session:
#         yield session
#
#     await async_session_maker.rollback()
#     await trans.rollback()
#     await async_session_maker.remove()
#
#
# @pytest.mark.asyncio
# async def test_get(async_session_maker, migrate_db):
#     await migrate_db
#     async with async_session_maker() as async_session:
#         await async_session.execute(
#             "INSERT INTO items (id, name, quantity) VALUES "
#             '(0, "crowbar", 13),'
#             '(1, "lamp", 94),'
#             '(2, "dull axe", 72)'
#         )
#         expected = models.Item(id=1, name="lamp", quantity=94)
#
#         result = await ItemRepository.get(async_session, pk=1)
#
#         assert result == expected
