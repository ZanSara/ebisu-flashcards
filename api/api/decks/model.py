from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.database import Base


class Deck(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    
    tags = Column(Integer, ForeignKey("tags.id"))

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="decks")
