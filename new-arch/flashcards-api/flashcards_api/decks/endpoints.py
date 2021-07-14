from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from flashcards_api.database import get_db
from flashcards_api.decks import operations
from flashcards_api.decks.schema import Deck, DeckCreate



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
    db_deck = operations.check_name_duplication(db, name=deck.name, owner_id=deck.owner_id)
    if db_deck:
        raise HTTPException(status_code=400, detail="A Deck with this name exists already for this user")
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

