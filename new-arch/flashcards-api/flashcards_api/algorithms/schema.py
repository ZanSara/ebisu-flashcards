from typing import Any, Optional

from pydantic import BaseModel


class Algorithm(BaseModel):
    name: str
    description: str


ALGORITHMS = {
    "Random Order": Algorithm(
                        name="Random Order", 
                        description="Random Order Algorithm"), 
    "Ebisu": Algorithm(
                        name="Ebisu", 
                        description="Ebisu Algorithm")
}