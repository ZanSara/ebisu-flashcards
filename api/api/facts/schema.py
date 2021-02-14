from typing import List, Optional

from pydantic import BaseModel


class FactBase(BaseModel):
    title: str
    description: Optional[str] = None


class FactCreate(FactBase):
    pass


class Fact(FactBase):
    id: int

    class Config:
        orm_mode = True
