from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from flashcards_api.database import Base


# Using single table inheritance here: https://docs.sqlalchemy.org/en/14/orm/inheritance.html#single-table-inheritance

class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    
    tags = Column(Integer, ForeignKey("tags.id"))

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="decks")

    algorithm = Column(String(50)) 

    __mapper_args__ = {
        'polymorphic_on': algorithm ,
        'polymorphic_identity':'deck'
    }


class RandomOrderDeck(Deck):
    unseen_cards_first = Column(Boolean)
    identical_cards_never_near = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity':'Random Order'
    }


class EbisuDeck(Deck):
    starting_alpha = Column(Float)
    starting_beta = Column(Float)
    starting_t = Column(Float)
    time_unit_in_minutes = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity':'Ebisu'
    }
