from sqlalchemy.orm import Session

from flashcards_api.templates.model import Template as TemplateModel
from flashcards_api.templates.schema import TemplateCreate



def get_templates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TemplateModel).offset(skip).limit(limit).all()


def get_template(db: Session, template_id: int):
    return db.query(TemplateModel).filter(TemplateModel.id == template_id).first()


# def create_template(db: Session, template: TemplateCreate):
#     db_template = TemplateModel(email=template.email, hashed_password=fake_hashed_password)
#     db.add(db_template)
#     db.commit()
#     db.refresh(db_template)
#     return db_template


# def create_template_item(db: Session, item: schemas.ItemCreate, template_id: int):
#     db_item = models.Item(**item.dict(), owner_id=template_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item