from typing import List, Optional

from pydantic import BaseModel


class DeckBase(BaseModel):
    title: str
    description: Optional[str] = None


class DeckCreate(DeckBase):
    pass


class Deck(DeckBase):
    id: int

    class Config:
        orm_mode = True
