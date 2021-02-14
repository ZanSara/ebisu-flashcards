from typing import List, Optional

from pydantic import BaseModel


class AlgorithmBase(BaseModel):
    title: str
    description: Optional[str] = None


class Algorithm(AlgorithmBase):
    id: int

    class Config:
        orm_mode = True
