from sqlalchemy.orm import Session

from flashcards_api.cards.model import Card as CardModel
from flashcards_api.cards.schema import CardCreate



def get_next_card(db: Session):
    pass
    #return db.query(CardModel).offset(skip).limit(limit).all()


def save_review_results(db: Session, card_id: int, review_results):
    pass
    #return db.query(CardModel).filter(CardModel.id == card_id).first()
