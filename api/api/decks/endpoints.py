from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.main import get_db
from api.decks import operations
from api.decks.schema import Deck, DeckCreate



router = APIRouter(
    prefix="/decks",
    tags=["decks"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Deck])
def get_decks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return operations.get_decks(db, skip=skip, limit=limit)


@router.post("/", response_model=Deck)
def create_deck(deck: DeckCreate, db: Session = Depends(get_db)):
    db_deck = operations.get_deck_by_email(db, email=deck.email)
    if db_deck:
        raise HTTPException(status_code=400, detail="Email already registered")
    return operations.create_deck(db=db, deck=deck)


@router.get("/{deck_id}", response_model=Deck)
def get_deck(deck_id: int, db: Session = Depends(get_db)):
    db_deck = operations.get_deck(db, deck_id=deck_id)
    if db_deck is None:
        raise HTTPException(status_code=404, detail="Deck not found")
    return db_deck


@router.put("/{deck_id}", response_model=Deck)
def edit_deck(deck_id: int, db: Session = Depends(get_db)):
    pass
    # db_deck = operations.get_deck(db, deck_id=deck_id)
    # if db_deck is None:
    #     raise HTTPException(status_code=404, detail="Deck not found")
    # return db_deck

@router.delete("/{deck_id}", response_model=Deck)
def delete_deck(deck_id: int, db: Session = Depends(get_db)):
    pass
    # db_deck = operations.get_deck(db, deck_id=deck_id)
    # if db_deck is None:
    #     raise HTTPException(status_code=404, detail="Deck not found")
    # return db_deck

