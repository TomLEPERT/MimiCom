from enum import Enum
from typing import List, Optional, Set

class ForceMode(str, Enum):
    none = "none"
    all = "all"
    email = "email"
    telephone = "telephone"
    rows = "rows"


def as_set(values: Optional[List[int]]) -> Set[int]:
    return set(values or [])
