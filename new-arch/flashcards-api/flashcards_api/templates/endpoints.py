from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from flashcards_api.database import get_db
from flashcards_api.templates import operations
from flashcards_api.templates.schema import Template



router = APIRouter(
    prefix="/templates",
    tags=["templates"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Template])
def get_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return operations.get_templates(db, skip=skip, limit=limit)


@router.get("/{template_id}", response_model=Template)
def get_template(template_id: int, db: Session = Depends(get_db)):
    db_template = operations.get_template(db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="Template not found")
    return db_template
