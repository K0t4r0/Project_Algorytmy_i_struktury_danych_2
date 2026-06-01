from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Dwarf:
    id: int
    name: str
    skills: List[str]
    home_pos: Tuple[int, int]

@dataclass
class Mine:
    id: str
    mine_type: str
    capacity: int
    pos: Tuple[int, int]

@dataclass
class BorderGuard:
    id: int
    name: str
    loudness: int
    position_meters: float = 0.0
    edge_index: int = -1