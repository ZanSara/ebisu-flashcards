from sqlalchemy.orm import Session

from api.algorithms.model import Algorithm as AlgorithmModel



def get_algorithms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AlgorithmModel).offset(skip).limit(limit).all()


def get_algorithm(db: Session, algorithm_id: int):
    return db.query(AlgorithmModel).filter(AlgorithmModel.id == algorithm_id).first()
