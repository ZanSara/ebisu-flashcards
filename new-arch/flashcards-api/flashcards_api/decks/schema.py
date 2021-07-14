from typing import List, Optional

from pydantic import BaseModel

from flashcards_api.tags.schema import Tag
from flashcards_api.users.schema import User
from flashcards_api.algorithms.schema import Algorithm
from flashcards_api.cards.schema import Card



class DeckBase(BaseModel):
    name: str
    description: str
    tags: Optional[List[Tag]]
    owner_id: int
    algorithm_name: str

class RandomOrderDeckBase(DeckBase):
    unseen_cards_first: bool
    identical_cards_never_near: bool

class EbisuDeckBase(DeckBase):
    starting_alpha: float
    starting_beta: float
    starting_t: float
    time_unit_in_minutes: int



class DeckCreate(DeckBase):
    pass

class RandomOrderDeckCreate(RandomOrderDeckBase):
    pass

class EbisuDeckCreate(EbisuDeckBase):
    pass



class Deck(DeckBase):
    id: int

    class Config:
        orm_mode = True

class RandomOrderDeck(Deck, RandomOrderDeckBase):
    pass

class EbisuDeck(Deck, EbisuDeckBase):
    pass
