from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import get_session
from db import models
from db.repository import ItemRepository

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/item/{item_id}", response_model=models.Item)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    try:
        return await ItemRepository.get(session, item_id)
    except Exception as exc:
        raise HTTPException(404, detail=str(exc))


@app.post("/item", status_code=201)
async def create_item(item: models.ItemCreate, session: AsyncSession = Depends(get_session)):
    try:
        await ItemRepository.add(session, item)
        await session.commit()
    except Exception as exc:
        raise HTTPException(400, detail=str(exc))
