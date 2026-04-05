from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Dwarf:
    id: int
    name: str
    skills: List[str]
    value: int
    home_pos: Tuple[int, int]

@dataclass
class Mine:
    id: str
    mine_type: str
    capacity: int
    pos: Tuple[int, int]