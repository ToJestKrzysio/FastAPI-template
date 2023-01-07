from __future__ import annotations

import abc

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(abc.ABC):

    @staticmethod
    async def get(session: AsyncSession, pk: any) -> BaseModel:
        raise NotImplementedError

    @staticmethod
    async def add(session: AsyncSession, obj: BaseModel) -> None:
        raise NotImplementedError
