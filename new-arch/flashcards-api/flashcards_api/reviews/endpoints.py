from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from flashcards_api.database import get_db
from flashcards_api.reviews import operations
from flashcards_api.cards.schema import Card
from flashcards_api.reviews.schema import ReviewCreate


router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=Card)
def next_card(db: Session = Depends(get_db)):
    return operations.get_next_card(db=db)


@router.post("/", response_model=Card)
def save_and_next_card(review: ReviewCreate, db: Session = Depends(get_db)):
    operations.save_review_results(db=db, review=review)
    return operations.get_next_card(db=db)
