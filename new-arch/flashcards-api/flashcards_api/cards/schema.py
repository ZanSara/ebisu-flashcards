from typing import List, Optional

from pydantic import BaseModel


class CardBase(BaseModel):
    pass
    # question: Fact
    # answer: Fact
    # tags: List[Tag]
    # decks: List[Deck]


class CardCreate(CardBase):
    pass


class Card(CardBase):
    id: int

    class Config:
        orm_mode = True
