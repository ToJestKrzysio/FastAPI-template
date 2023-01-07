from __future__ import annotations

import abc

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import models, orm


class AbstractRepository(abc.ABC):

    @staticmethod
    async def get(session: AsyncSession, pk: any) -> BaseModel:
        raise NotImplementedError

    @staticmethod
    async def add(session: AsyncSession, obj: BaseModel) -> None:
        raise NotImplementedError


class ItemRepository(AbstractRepository):

    @staticmethod
    async def get(session: AsyncSession, pk: int) -> models.Item:
        stmt = select(orm.Item).where(orm.Item.id == pk)
        results = await session.execute(stmt)
        instance = results.scalar_one()
        return models.Item.from_orm(instance)

    @staticmethod
    async def add(session: AsyncSession, obj: models.ItemCreate) -> None:
        item = orm.Item(**obj.dict())
        session.add(item)
