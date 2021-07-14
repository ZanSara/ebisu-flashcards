from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from flashcards_api.database import get_db
from flashcards_api.cards import operations
from flashcards_api.cards.schema import Card, CardCreate



router = APIRouter(
    prefix="/cards",
    tags=["cards"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Card])
def get_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return operations.get_cards(db, skip=skip, limit=limit)


@router.post("/", response_model=Card)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    db_card = operations.get_card_by_email(db, email=card.email)
    if db_card:
        raise HTTPException(status_code=400, detail="Email already registered")
    return operations.create_card(db=db, card=card)


@router.get("/{card_id}", response_model=Card)
def get_card(card_id: int, db: Session = Depends(get_db)):
    db_card = operations.get_card(db, card_id=card_id)
    if db_card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return db_card


@router.put("/{card_id}", response_model=Card)
def edit_card(card_id: int, db: Session = Depends(get_db)):
    pass
    # db_card = operations.get_card(db, card_id=card_id)
    # if db_card is None:
    #     raise HTTPException(status_code=404, detail="Card not found")
    # return db_card

@router.delete("/{card_id}", response_model=Card)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    pass
    # db_card = operations.get_card(db, card_id=card_id)
    # if db_card is None:
    #     raise HTTPException(status_code=404, detail="Card not found")
    # return db_card

