from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from flashcards_api.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)  # Either an ALT text for a file or the text content itself
    url = Column(String)  # CAN BE EMPTY: Might contain a url to a file if it's an audio or image resource

    fact_id = Column(Integer, ForeignKey("Fact"))
    fact = relationship("Facts", back_populates="resources")