from dataclasses import dataclass, field
from typing import List

@dataclass
class House:
    number: int
    lord: str = ""
    planets: List[str] = field(default_factory=list)
