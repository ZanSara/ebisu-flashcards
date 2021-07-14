from sqlalchemy.orm import Session

from flashcards_api.decks.model import Deck as DeckModel
from flashcards_api.decks.schema import DeckCreate



def get_decks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeckModel).offset(skip).limit(limit).all()


def get_deck(db: Session, deck_id: int):
    return db.query(DeckModel).filter(DeckModel.id == deck_id).first()


def check_name_duplication(db: Session, name: str, owner_id: int):
    return db.query(DeckModel).filter(DeckModel.owner.id == owner_id).filter(DeckModel.name == name).first()


# def create_deck(db: Session, deck: DeckCreate):
#     db_deck = DeckModel(email=deck.email, hashed_password=fake_hashed_password)
#     db.add(db_deck)
#     db.commit()
#     db.refresh(db_deck)
#     return db_deck


# def create_deck_item(db: Session, item: schemas.ItemCreate, deck_id: int):
#     db_item = models.Item(**item.dict(), owner_id=deck_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item