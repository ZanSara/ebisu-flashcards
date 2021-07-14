from sqlalchemy.orm import Session

from flashcards_api.facts.model import Fact as FactModel
from flashcards_api.facts.schema import FactCreate



def get_facts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(FactModel).offset(skip).limit(limit).all()


def get_fact(db: Session, fact_id: int):
    return db.query(FactModel).filter(FactModel.id == fact_id).first()


# def create_fact(db: Session, fact: FactCreate):
#     db_fact = FactModel(email=fact.email, hashed_password=fake_hashed_password)
#     db.add(db_fact)
#     db.commit()
#     db.refresh(db_fact)
#     return db_fact


# def create_fact_item(db: Session, item: schemas.ItemCreate, fact_id: int):
#     db_item = models.Item(**item.dict(), owner_id=fact_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item