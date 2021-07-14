from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from flashcards_api.database import get_db
from flashcards_api.tags import operations
from flashcards_api.tags.schema import Tag, TagCreate



router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Tag])
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return operations.get_tags(db, skip=skip, limit=limit)


@router.post("/", response_model=Tag)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = operations.get_tag_by_email(db, email=tag.email)
    if db_tag:
        raise HTTPException(status_code=400, detail="Email already registered")
    return operations.create_tag(db=db, tag=tag)


@router.get("/{tag_id}", response_model=Tag)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = operations.get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.put("/{tag_id}", response_model=Tag)
def edit_tag(tag_id: int, db: Session = Depends(get_db)):
    pass
    # db_tag = operations.get_tag(db, tag_id=tag_id)
    # if db_tag is None:
    #     raise HTTPException(status_code=404, detail="Tag not found")
    # return db_tag

@router.delete("/{tag_id}", response_model=Tag)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    pass
    # db_tag = operations.get_tag(db, tag_id=tag_id)
    # if db_tag is None:
    #     raise HTTPException(status_code=404, detail="Tag not found")
    # return db_tag

