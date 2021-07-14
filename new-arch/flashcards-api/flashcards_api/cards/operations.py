from sqlalchemy.orm import Session

from flashcards_api.cards.model import Card as CardModel
from flashcards_api.cards.schema import CardCreate



def get_cards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CardModel).offset(skip).limit(limit).all()


def get_card(db: Session, card_id: int):
    return db.query(CardModel).filter(CardModel.id == card_id).first()


# def create_card(db: Session, card: CardCreate):
#     db_card = CardModel(email=card.email, hashed_password=fake_hashed_password)
#     db.add(db_card)
#     db.commit()
#     db.refresh(db_card)
#     return db_card


# def create_card_item(db: Session, item: schemas.ItemCreate, card_id: int):
#     db_item = models.Item(**item.dict(), owner_id=card_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item