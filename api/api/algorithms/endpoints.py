from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.main import get_db
from api.algorithms import operations
from api.algorithms.schema import Algorithm



router = APIRouter(
    prefix="/algorithms",
    tags=["algorithms"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Algorithm])
def get_algorithms():
    return operations.get_algorithms()


@router.get("/{algorithm_id}", response_model=Algorithm)
def get_algorithm(algorithm_id: int):
    algorithm = operations.get_algorithm(algorithm_id=algorithm_id)
    if algorithm is None:
        raise HTTPException(status_code=404, detail="Algorithm not found")
    return algorithm
