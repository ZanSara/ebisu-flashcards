from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.main import get_db
from api.reviews import operations
from api.cards.schema import Card
from api.reviews.schema import ReviewCreate


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
