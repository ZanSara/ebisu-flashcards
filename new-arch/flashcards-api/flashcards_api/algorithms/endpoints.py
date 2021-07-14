from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from flashcards_api.database import get_db
from flashcards_api.algorithms import operations
from flashcards_api.algorithms.schema import Algorithm



router = APIRouter(
    prefix="/algorithms",
    tags=["algorithms"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Algorithm])
def get_algorithms():
    return operations.get_algorithms()


@router.get("/{algorithm_name}", response_model=Algorithm)
def get_algorithm(algorithm_name: str):
    algorithm = operations.get_algorithm(algorithm_name=algorithm_name)
    if algorithm is None:
        raise HTTPException(status_code=404, detail="Algorithm not found")
    return algorithm
