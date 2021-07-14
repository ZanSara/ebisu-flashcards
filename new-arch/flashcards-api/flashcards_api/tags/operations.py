from sqlalchemy.orm import Session

from flashcards_api.tags.model import Tag as TagModel
from flashcards_api.tags.schema import TagCreate



def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TagModel).offset(skip).limit(limit).all()


def get_tag(db: Session, tag_id: int):
    return db.query(TagModel).filter(TagModel.id == tag_id).first()


# def create_tag(db: Session, tag: TagCreate):
#     db_tag = TagModel(email=tag.email, hashed_password=fake_hashed_password)
#     db.add(db_tag)
#     db.commit()
#     db.refresh(db_tag)
#     return db_tag


# def create_tag_item(db: Session, item: schemas.ItemCreate, tag_id: int):
#     db_item = models.Item(**item.dict(), owner_id=tag_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item