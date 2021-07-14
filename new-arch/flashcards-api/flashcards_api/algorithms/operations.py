from sqlalchemy.orm import Session

from flashcards_api.algorithms.schema import Algorithm, ALGORITHMS



def get_algorithms():
    return list(ALGORITHMS.values())


def get_algorithm(algorithm_name: str):
    return ALGORITHMS.get(algorithm_name)
