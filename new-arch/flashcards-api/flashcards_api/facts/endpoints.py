from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from flashcards_api.database import get_db
from flashcards_api.facts import operations
from flashcards_api.facts.schema import Fact, FactCreate



router = APIRouter(
    prefix="/facts",
    tags=["facts"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Fact])
def get_facts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return operations.get_facts(db, skip=skip, limit=limit)


@router.post("/", response_model=Fact)
def create_fact(fact: FactCreate, db: Session = Depends(get_db)):
    db_fact = operations.get_fact_by_email(db, email=fact.email)
    if db_fact:
        raise HTTPException(status_code=400, detail="Email already registered")
    return operations.create_fact(db=db, fact=fact)


@router.get("/{fact_id}", response_model=Fact)
def get_fact(fact_id: int, db: Session = Depends(get_db)):
    db_fact = operations.get_fact(db, fact_id=fact_id)
    if db_fact is None:
        raise HTTPException(status_code=404, detail="Fact not found")
    return db_fact


@router.put("/{fact_id}", response_model=Fact)
def edit_fact(fact_id: int, db: Session = Depends(get_db)):
    pass
    # db_fact = operations.get_fact(db, fact_id=fact_id)
    # if db_fact is None:
    #     raise HTTPException(status_code=404, detail="Fact not found")
    # return db_fact

@router.delete("/{fact_id}", response_model=Fact)
def delete_fact(fact_id: int, db: Session = Depends(get_db)):
    pass
    # db_fact = operations.get_fact(db, fact_id=fact_id)
    # if db_fact is None:
    #     raise HTTPException(status_code=404, detail="Fact not found")
    # return db_fact

