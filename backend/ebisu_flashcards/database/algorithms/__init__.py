from ebisu_flashcards.database.algorithms.algorithm import Algorithm
from ebisu_flashcards.database.algorithms.random_order import RandomOrder
from ebisu_flashcards.database.algorithms.ebisu import Ebisu


ALGORITHM_MAPPING = {
    "Random Order": RandomOrder,
    "Ebisu": Ebisu,
}


def algorithm_engine(deck: 'Deck') -> 'Algorithm':
    """ Given the algorithm name, returns a suitable engine """
    try:
        return ALGORITHM_MAPPING[deck.algorithm](deck)
    except KeyError:
        raise ValueError("Algorithm name unknown: {}".format(deck.algorithm))


def import_from_file(file_path: str) -> 'Deck':
    """ Loads a new deck from a .zip file and adds it to the decks list. """
    raise NotImplementedError("TODO")
