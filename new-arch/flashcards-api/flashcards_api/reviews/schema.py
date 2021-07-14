from typing import List, Optional

from pydantic import BaseModel


class ReviewBase(BaseModel):
    title: str
    description: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True
