from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    id: Optional[int]
    name: str
    quantity: int

    class Config:
        orm_mode = True


class ItemCreate(BaseModel):
    name: str
    quantity: int
