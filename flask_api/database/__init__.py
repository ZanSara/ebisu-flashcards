from . import algorithms


ALGORITHM_MAPPING = {
    "Random Order": algorithms.RandomOrder,
    "Ebisu": algorithms.Ebisu,
}

def algorithm_engine(name: str) -> algorithms.Algorithm:
    """ Given the algorithm name, returns a suitable engine """
    try:
        return ALGORITHM_MAPPING[name]()
    except KeyError:
        raise ValueError("Algorithm name unknown: {}".format(name))


def import_from_file(file_path: str) -> 'Deck':
    """ Loads a new deck from a .zip file and adds it to the decks list. """
    raise NotImplementedError("TODO")

