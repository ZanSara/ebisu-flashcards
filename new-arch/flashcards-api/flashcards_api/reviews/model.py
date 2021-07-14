from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from flashcards_api.models import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    card = relationship("Card")
    user = relationship("User")
    algorithm = relationship("Algorithm")
    #time = Column(models.DateTimeField(_(""), auto_now=False, auto_now_add=False))
    result = Column(String)  # FIXME depends on the algorithm to some degree (think Anki)
