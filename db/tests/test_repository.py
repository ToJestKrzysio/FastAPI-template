import pytest

from db import models
from db.repository import ItemRepository


@pytest.mark.asyncio
async def test_get(async_session_maker, migrated_db):
    async with async_session_maker() as session:
        await session.execute(
            "INSERT INTO items (id, name, quantity) VALUES "
            '(0, "crowbar", 13),'
            '(1, "lamp", 94),'
            '(2, "dull axe", 72)'
        )
        expected = models.Item(id=1, name="lamp", quantity=94)

        result = await ItemRepository.get(session, pk=1)

        assert result == expected


@pytest.mark.asyncio
async def test_if_data_from_previous_test_was_removed_from_db(async_session_maker, migrated_db):
    async with async_session_maker() as session:
        await session.execute(
            "INSERT INTO items (id, name, quantity) VALUES "
            '(0, "rubber duck", 31),'
            '(1, "fluffy rabbit", 14)'
        )
        await session.commit()

        expected = models.Item(id=1, name="fluffy rabbit", quantity=14)

        result = await ItemRepository.get(session, pk=1)

        assert result == expected
