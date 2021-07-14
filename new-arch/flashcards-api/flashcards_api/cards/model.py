from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from flashcards_api.database import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    question = relationship("Fact")
    answer = relationship("Fact")
    tags = relationship("Tag")
    decks = relationship("Deck", back_populates="cards")  # The same card can belong to multiple decks