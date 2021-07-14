from typing import List, Optional

from pydantic import BaseModel


class TemplateBase(BaseModel):
    title: str
    description: Optional[str] = None


class TemplateCreate(TemplateBase):
    pass


class Template(TemplateBase):
    id: int

    class Config:
        orm_mode = True
