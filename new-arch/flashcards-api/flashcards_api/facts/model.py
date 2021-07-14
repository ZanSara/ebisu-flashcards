from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from flashcards_api.database import Base


class Fact(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    template = Column(Integer, ForeignKey("templates.id"))
    resources = relationship("Resources", back_populates="facts")
    cards = relationship("Card")